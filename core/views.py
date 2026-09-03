"""
Admin statistics endpoint.
"""
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from bookings.models import Booking

User = get_user_model()


class AdminStatsView(APIView):
    """
    GET /api/stats/ — dashboard statistics for admin users only.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_events = Event.objects.count()
        total_bookings = Booking.objects.count()
        confirmed_bookings = Booking.objects.filter(status='confirmed').count()
        cancelled_bookings = Booking.objects.filter(status='cancelled').count()
        total_users = User.objects.filter(is_staff=False).count()

        # Total tickets sold = sum of quantities for confirmed bookings
        from django.db.models import Sum
        tickets_sold = (
            Booking.objects
            .filter(status='confirmed')
            .aggregate(total=Sum('quantity'))['total'] or 0
        )

        # Revenue = sum of (price * quantity) for confirmed bookings
        from django.db.models import F
        revenue = (
            Booking.objects
            .filter(status='confirmed')
            .annotate(booking_total=F('event__price') * F('quantity'))
            .aggregate(total=Sum('booking_total'))['total'] or 0
        )

        # Recent bookings (last 5)
        from bookings.serializers import BookingSerializer
        recent_bookings = Booking.objects.select_related('event', 'user').order_by('-booking_date')[:5]
        recent_data = BookingSerializer(recent_bookings, many=True, context={'request': request}).data

        return Response({
            'total_events': total_events,
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_users': total_users,
            'tickets_sold': tickets_sold,
            'revenue': float(revenue),
            'recent_bookings': recent_data,
        })
