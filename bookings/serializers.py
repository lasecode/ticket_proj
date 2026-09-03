"""
Booking serializers.
"""
from rest_framework import serializers
from events.models import Event
from events.serializers import EventListSerializer
from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    """Used when creating a new booking — validates quantity and availability."""

    class Meta:
        model = Booking
        fields = ['event', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('You must book at least 1 ticket.')
        return value

    def validate(self, data):
        event = data['event']
        quantity = data['quantity']

        if quantity > event.available_tickets:
            raise serializers.ValidationError({
                'quantity': (
                    f'Only {event.available_tickets} ticket(s) available. '
                    f'You requested {quantity}.'
                )
            })
        return data


class BookingSerializer(serializers.ModelSerializer):
    """Full read serializer — includes event summary and computed fields."""

    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateField(source='event.date', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    event_category = serializers.CharField(source='event.category', read_only=True)
    total_price = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'event', 'event_title', 'event_date',
            'event_location', 'event_category', 'quantity', 'total_price',
            'status', 'status_display', 'booking_date',
        ]
        read_only_fields = [
            'booking_reference', 'booking_date', 'status',
        ]
