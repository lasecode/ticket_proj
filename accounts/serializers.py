"""
Serializers for user registration, login, and profile.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new user registration."""

    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Read and update the authenticated user's profile."""

    full_name = serializers.ReadOnlyField()
    total_bookings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'bio', 'is_staff', 'date_joined', 'total_bookings',
        ]
        read_only_fields = ['email', 'is_staff', 'date_joined']

    def get_total_bookings(self, obj):
        return obj.bookings.filter(status='confirmed').count()


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight user info used inside other serializers."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']
