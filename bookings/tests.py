"""
Tests for bookings app:
- Booking creation & ticket decrement
- Overbooking prevention
- Booking cancellation & ticket return
- Permission checks
"""
from datetime import date, time, timedelta
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from events.models import Event
from bookings.models import Booking

User = get_user_model()


class BookingsAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='Password123!',
            first_name='User',
            last_name='One',
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='Password123!',
            first_name='User',
            last_name='Two',
        )
        self.event = Event.objects.create(
            title='Exclusive Tech Meetup',
            description='Limited seating event',
            location='Lagos Hub',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            category=Event.Category.TECHNOLOGY,
            price=10000,
            total_tickets=10,
            available_tickets=10,
        )

    def test_booking_creation_decreases_availability(self):
        """Test booking 3 tickets decreases available_tickets from 10 to 7."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('booking-list-create')
        data = {'event': self.event.id, 'quantity': 3}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('EVT-', response.data['booking_reference'])

        # Check DB state
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_tickets, 7)

    def test_prevent_overbooking(self):
        """Test requesting more tickets than available fails."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('booking-list-create')
        data = {'event': self.event.id, 'quantity': 15}  # Only 10 available

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Availability must remain unchanged
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_tickets, 10)

    def test_booking_cancellation_increases_availability(self):
        """Test cancelling a booking returns tickets to available pool."""
        self.client.force_authenticate(user=self.user1)
        url_create = reverse('booking-list-create')

        # First book 4 tickets (10 -> 6)
        res = self.client.post(url_create, {'event': self.event.id, 'quantity': 4}, format='json')
        booking_id = res.data['id']
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_tickets, 6)

        # Now cancel the booking
        url_detail = reverse('booking-detail', kwargs={'pk': booking_id})
        res_cancel = self.client.delete(url_detail)
        self.assertEqual(res_cancel.status_code, status.HTTP_200_OK)
        self.assertEqual(res_cancel.data['status'], 'cancelled')

        # Tickets returned: 6 + 4 = 10
        self.event.refresh_from_db()
        self.assertEqual(self.event.available_tickets, 10)

    def test_user_cannot_cancel_others_booking(self):
        """Test that user2 cannot cancel user1's booking."""
        self.client.force_authenticate(user=self.user1)
        url_create = reverse('booking-list-create')
        res = self.client.post(url_create, {'event': self.event.id, 'quantity': 2}, format='json')
        booking_id = res.data['id']

        # Authenticate as user2
        self.client.force_authenticate(user=self.user2)
        url_detail = reverse('booking-detail', kwargs={'pk': booking_id})
        res_cancel = self.client.delete(url_detail)
        self.assertEqual(res_cancel.status_code, status.HTTP_404_NOT_FOUND)
