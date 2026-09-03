"""
Django Admin configuration for Event model.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin configuration for managing Events."""

    list_display = (
        'title', 'category_badge', 'date', 'time', 'location',
        'price_formatted', 'ticket_availability', 'is_featured', 'created_at',
    )
    list_filter = ('category', 'is_featured', 'date', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('date', 'time')
    date_hierarchy = 'date'
    list_editable = ('is_featured',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('General Information', {
            'fields': ('title', 'category', 'description', 'image', 'is_featured'),
        }),
        ('Event Schedule & Location', {
            'fields': ('date', 'time', 'location'),
        }),
        ('Ticketing', {
            'fields': ('price', 'total_tickets', 'available_tickets'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_as_featured', 'unmark_as_featured', 'reset_available_tickets']

    @admin.display(description='Category')
    def category_badge(self, obj):
        colors = {
            'concert': '#e94560',
            'technology': '#6c63ff',
            'business': '#2D6A4F',
            'sports': '#7F5AF0',
            'education': '#003566',
            'entertainment': '#CF1124',
        }
        color = colors.get(obj.category, '#6c63ff')
        return format_html(
            '<span style="background-color:{}; color:#fff; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{}</span>',
            color, obj.get_category_display()
        )

    @admin.display(description='Price')
    def price_formatted(self, obj):
        return f"₦{obj.price:,.2f}"

    @admin.display(description='Tickets Available')
    def ticket_availability(self, obj):
        color = 'green'
        if obj.available_tickets == 0:
            color = 'red'
        elif obj.available_tickets < 10:
            color = 'orange'
        return format_html(
            '<strong style="color:{};">{}/{}</strong>',
            color, obj.available_tickets, obj.total_tickets
        )

    @admin.action(description='Mark selected events as Featured')
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} event(s) marked as featured.")

    @admin.action(description='Unmark selected events as Featured')
    def unmark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} event(s) unmarked as featured.")

    @admin.action(description='Reset available tickets to total tickets')
    def reset_available_tickets(self, request, queryset):
        count = 0
        for event in queryset:
            event.available_tickets = event.total_tickets
            event.save(update_fields=['available_tickets'])
            count += 1
        self.message_user(request, f"Available tickets reset for {count} event(s).")
