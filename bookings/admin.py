"""
Django Admin configuration for Booking model.
"""
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html
from .models import Booking
from events.models import Event


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for managing Bookings."""

    list_display = (
        'booking_reference_styled', 'user_email', 'event_title',
        'quantity', 'total_price_formatted', 'status_badge', 'booking_date',
    )
    list_filter = ('status', 'booking_date', 'event__category')
    search_fields = ('booking_reference', 'user__email', 'user__first_name', 'user__last_name', 'event__title')
    ordering = ('-booking_date',)
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_reference', 'booking_date')

    fieldsets = (
        ('Booking Details', {
            'fields': ('booking_reference', 'user', 'event', 'quantity', 'status'),
        }),
        ('Timestamp', {
            'fields': ('booking_date',),
        }),
    )

    actions = ['cancel_selected_bookings', 'confirm_selected_bookings']

    @admin.display(description='Reference', ordering='booking_reference')
    def booking_reference_styled(self, obj):
        return format_html(
            '<code style="background:#f4f4f4; padding:3px 6px; border-radius:4px; font-weight:bold; color:#6c63ff;">{}</code>',
            obj.booking_reference
        )

    @admin.display(description='User', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Event', ordering='event__title')
    def event_title(self, obj):
        return obj.event.title

    @admin.display(description='Total Price')
    def total_price_formatted(self, obj):
        return f"₦{obj.total_price:,.2f}"

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.status == Booking.Status.CONFIRMED:
            return format_html(
                '<span style="background-color:#10B981; color:#fff; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:bold;">Confirmed</span>'
            )
        return format_html(
            '<span style="background-color:#EF4444; color:#fff; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:bold;">Cancelled</span>'
        )

    @admin.action(description='Cancel selected bookings and return tickets to event')
    def cancel_selected_bookings(self, request, queryset):
        cancelled_count = 0
        with transaction.atomic():
            for booking in queryset.filter(status=Booking.Status.CONFIRMED):
                event = Event.objects.select_for_update().get(pk=booking.event_id)
                event.available_tickets += booking.quantity
                event.save(update_fields=['available_tickets'])

                booking.status = Booking.Status.CANCELLED
                booking.save(update_fields=['status'])
                cancelled_count += 1

        self.message_user(request, f"{cancelled_count} booking(s) cancelled and tickets returned to inventory.")

    @admin.action(description='Confirm selected bookings (if cancelled, deducts tickets)')
    def confirm_selected_bookings(self, request, queryset):
        confirmed_count = 0
        skipped_count = 0
        with transaction.atomic():
            for booking in queryset.filter(status=Booking.Status.CANCELLED):
                event = Event.objects.select_for_update().get(pk=booking.event_id)
                if event.available_tickets >= booking.quantity:
                    event.available_tickets -= booking.quantity
                    event.save(update_fields=['available_tickets'])

                    booking.status = Booking.Status.CONFIRMED
                    booking.save(update_fields=['status'])
                    confirmed_count += 1
                else:
                    skipped_count += 1

        msg = f"{confirmed_count} booking(s) confirmed."
        if skipped_count:
            msg += f" {skipped_count} booking(s) skipped due to insufficient ticket availability."
        self.message_user(request, msg)
