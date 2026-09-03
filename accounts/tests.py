"""
Tests for accounts app: User registration, login, and profile.
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsAPITests(APITestCase):

    def test_user_registration(self):
        """Test creating a new user account via API."""
        url = reverse('auth-register')
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'Password123!',
            'password2': 'Password123!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        """Test logging in with valid credentials."""
        User.objects.create_user(
            email='testlogin@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
        )
        url = reverse('auth-login')
        data = {
            'email': 'testlogin@example.com',
            'password': 'TestPassword123!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_profile_authenticated(self):
        """Test fetching profile for logged in user."""
        user = User.objects.create_user(
            email='profile@example.com',
            password='Password123!',
            first_name='Profile',
            last_name='Owner',
        )
        self.client.force_authenticate(user=user)
        url = reverse('auth-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'profile@example.com')
