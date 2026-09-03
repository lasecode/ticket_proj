"""
Booking views — create, list, retrieve, and cancel bookings.

Key safety feature: ticket decrement/increment is wrapped in a database
transaction with select_for_update() to prevent race conditions.
"""
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from events.models import Event


class BookingListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/bookings/ — list bookings (own for users, all for admins)
    POST /api/bookings/ — create a new booking
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admins see every booking
            return Booking.objects.select_related('event', 'user').all()
        # Regular users only see their own bookings
        return Booking.objects.select_related('event').filter(user=user)

    def create(self, request, *args, **kwargs):
        """
        Create a booking and decrement available_tickets atomically.
        Uses select_for_update so two simultaneous requests cannot
        both succeed when only one ticket remains.
        """
        serializer = BookingCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data['event'].id
        quantity = serializer.validated_data['quantity']

        with transaction.atomic():
            # Lock the event row for the duration of this transaction
            event = Event.objects.select_for_update().get(pk=event_id)

            # Re-check availability inside the transaction
            if quantity > event.available_tickets:
                return Response(
                    {'detail': f'Only {event.available_tickets} ticket(s) available.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Deduct the tickets
            event.available_tickets -= quantity
            event.save(update_fields=['available_tickets'])

            # Create the booking
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                quantity=quantity,
                status=Booking.Status.CONFIRMED,
            )

        response_serializer = BookingSerializer(booking, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BookingDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/bookings/<id>/ — retrieve a booking
    DELETE /api/bookings/<id>/ — cancel a booking (returns tickets)
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related('event', 'user').all()
        return Booking.objects.select_related('event').filter(user=user)

    def destroy(self, request, *args, **kwargs):
        """
        Cancel the booking and return the tickets to the event atomically.
        Only confirmed bookings can be cancelled.
        """
        booking = self.get_object()

        # Only the booking owner (or admin) can cancel
        if not request.user.is_staff and booking.user != request.user:
            raise PermissionDenied('You cannot cancel someone else\'s booking.')

        if booking.status == Booking.Status.CANCELLED:
            return Response(
                {'detail': 'This booking is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # Lock the event row
            event = Event.objects.select_for_update().get(pk=booking.event_id)

            # Return the tickets
            event.available_tickets += booking.quantity
            event.save(update_fields=['available_tickets'])

            # Mark booking as cancelled
            booking.status = Booking.Status.CANCELLED
            booking.save(update_fields=['status'])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
