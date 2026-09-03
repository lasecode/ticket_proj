"""
Booking model — links users to events with ticket management.
"""
import random
import string
from django.conf import settings
from django.db import models
from events.models import Event


def generate_booking_reference():
    """
    Generates a unique booking reference like EVT-8F4K29.
    Keeps trying until a unique one is found.
    """
    while True:
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choices(chars, k=6))
        reference = f'EVT-{suffix}'
        if not Booking.objects.filter(booking_reference=reference).exists():
            return reference


class Booking(models.Model):
    """Represents a ticket booking by a user for an event."""

    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    quantity = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CONFIRMED,
        db_index=True,
    )
    booking_reference = models.CharField(max_length=12, unique=True, editable=False)

    class Meta:
        db_table = 'bookings'
        ordering = ['-booking_date']

    def __str__(self):
        return f'{self.booking_reference} — {self.user.email} for {self.event.title}'

    def save(self, *args, **kwargs):
        # Auto-generate reference on first save
        if not self.booking_reference:
            self.booking_reference = generate_booking_reference()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.event.price * self.quantity
