"""
Serializers for the Event model.
"""
from rest_framework import serializers
from .models import Event


class EventListSerializer(serializers.ModelSerializer):
    """Compact serializer used in list views (cards on the home page)."""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    is_sold_out = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'image_url', 'location', 'date', 'time',
            'category', 'category_display', 'price', 'total_tickets',
            'available_tickets', 'is_sold_out', 'is_featured',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class EventDetailSerializer(serializers.ModelSerializer):
    """Full serializer used for event detail and create/update."""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    is_sold_out = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'image', 'image_url', 'location',
            'date', 'time', 'category', 'category_display', 'price',
            'total_tickets', 'available_tickets', 'is_sold_out', 'is_featured',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['available_tickets', 'created_at', 'updated_at']
        extra_kwargs = {'image': {'required': False, 'allow_null': True}}

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        # When creating a new event, available_tickets starts equal to total_tickets
        validated_data['available_tickets'] = validated_data['total_tickets']
        return super().create(validated_data)
