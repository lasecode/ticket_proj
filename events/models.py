"""
Event model — stores all event information.
"""
from django.db import models


class Event(models.Model):
    """Represents a ticketed event."""

    class Category(models.TextChoices):
        CONCERT = 'concert', 'Concert'
        TECHNOLOGY = 'technology', 'Technology'
        BUSINESS = 'business', 'Business'
        SPORTS = 'sports', 'Sports'
        EDUCATION = 'education', 'Education'
        ENTERTAINMENT = 'entertainment', 'Entertainment'

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    location = models.CharField(max_length=200, db_index=True)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.ENTERTAINMENT,
        db_index=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        ordering = ['date', 'time']

    def __str__(self):
        return f'{self.title} ({self.date})'

    @property
    def is_sold_out(self):
        return self.available_tickets == 0

    @property
    def image_url(self):
        """Returns a placeholder gradient URL if no image is uploaded."""
        if self.image:
            return self.image.url
        return None
