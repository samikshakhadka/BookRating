from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user3@example.com', password='password123', is_verified=True )
        self.superuser = User.objects.create_superuser(email='admin@example.com', password='admin123')
        print(f"User verification token: {self.user.verification_token}")
    
    def test_register_user(self):
        url = reverse('register')
        data = {'email': 'newuser3@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
    
    def test_verify_email(self):
        url = reverse('verify-email', kwargs={'verification_token': self.user.verification_token})
        response = self.client.get(url)
        print(f"Verify Email Response: {response.content}")  # Debugging statement
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
    
    def test_login(self):
        url = reverse('login')
        data = {'email': 'user3@example.com', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
    
    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('change-password')
        data = {'old_password': 'password123', 'new_password': 'newpassword123', 'confirm_password':'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
