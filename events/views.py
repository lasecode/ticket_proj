"""
Event API views — full CRUD with search and filtering.
"""
from django.utils import timezone
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event
from .serializers import EventListSerializer, EventDetailSerializer
from .permissions import IsAdminOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet providing list, create, retrieve, update, and destroy for events.

    - Anyone can list and view events.
    - Only admin/staff can create, edit, or delete events.
    """

    queryset = Event.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'price', 'created_at']
    ordering = ['date']

    def get_serializer_class(self):
        """Use the compact serializer for lists; full serializer otherwise."""
        if self.action == 'list':
            return EventListSerializer
        return EventDetailSerializer

    def get_queryset(self):
        """Apply optional query-string filters."""
        qs = Event.objects.all()

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)

        # Filter only upcoming events (today onward)
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() == 'true':
            qs = qs.filter(date__gte=timezone.now().date())

        # Filter by location (partial, case-insensitive)
        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(location__icontains=location)

        # Filter featured events
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            qs = qs.filter(is_featured=True)

        return qs

    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        """GET /api/events/categories/ — returns all available categories."""
        cats = [{'value': c[0], 'label': c[1]} for c in Event.Category.choices]
        return Response(cats)
