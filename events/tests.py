"""
Tests for events app: Event creation, retrieval, listing, permissions.
"""
from datetime import date, time, timedelta
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()


class EventsAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin_test@example.com',
            password='AdminPassword123!',
            first_name='Admin',
            last_name='User',
        )
        self.user = User.objects.create_user(
            email='regular_test@example.com',
            password='UserPassword123!',
            first_name='Regular',
            last_name='User',
        )
        self.event = Event.objects.create(
            title='Test Concert',
            description='A test concert event',
            location='Lagos',
            date=date.today() + timedelta(days=5),
            time=time(18, 0),
            category=Event.Category.CONCERT,
            price=5000,
            total_tickets=100,
            available_tickets=100,
        )

    def test_event_retrieval(self):
        """Test retrieving list and detail of events unauthenticated."""
        # List
        url = reverse('events-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Detail
        url_detail = reverse('events-detail', kwargs={'pk': self.event.id})
        response_detail = self.client.get(url_detail)
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data['title'], 'Test Concert')

    def test_admin_event_creation(self):
        """Test that admin user can create an event."""
        self.client.force_authenticate(user=self.admin)
        url = reverse('events-list')
        data = {
            'title': 'New Admin Event',
            'description': 'Description',
            'location': 'Abuja',
            'date': str(date.today() + timedelta(days=10)),
            'time': '10:00:00',
            'category': 'technology',
            'price': '3000.00',
            'total_tickets': 50,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['available_tickets'], 50)

    def test_regular_user_cannot_create_event(self):
        """Test that regular users are forbidden from creating events."""
        self.client.force_authenticate(user=self.user)
        url = reverse('events-list')
        data = {
            'title': 'Unauthorized Event',
            'description': 'Description',
            'location': 'Abuja',
            'date': str(date.today() + timedelta(days=10)),
            'time': '10:00:00',
            'category': 'technology',
            'price': '3000.00',
            'total_tickets': 50,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
