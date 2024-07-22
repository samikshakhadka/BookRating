import uuid
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

User = get_user_model()

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }

    @patch('apps.user.serializers.send_verification_email_task.delay')
    def test_register_user(self, mock_send_verification_email_task):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        mock_send_verification_email_task.assert_called_once()

class VerifyEmailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_verified=False,
            verification_token=uuid.uuid4()
        )
        self.url = reverse('verify-email', kwargs={'verification_token': self.user.verification_token})

    def test_verify_email(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_verified=True
        )
        self.url = reverse('login')
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

    def test_login_user(self):
        response = self.client.post(self.url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_verified=True
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('logout')

    def test_logout_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class ChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_verified=True
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('change-password')
        self.password_data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword',
            'confirm_password': 'newpassword'
        }

    def test_change_password(self):
        response = self.client.post(self.url, self.password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))





















# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token

# User = get_user_model()

# class UserViewSetTests(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(email='user3@example.com', password='password123', is_verified=False )
#         self.superuser = User.objects.create_superuser(email='admin@example.com', password='admin123')
#         print(f"User verification token: {self.user.verification_token}")
    
#     def test_register_user(self):
#         url = reverse('register')
#         data = {'email': 'newuser3@example.com', 'password': 'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 3)
    
#     def test_verify_email(self):
#         url = reverse('verify-email', kwargs={'verification_token': self.user.verification_token})
#         response = self.client.get(url)
#         print(f"Verify Email Response: {response.content}")  # Debugging statement
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.is_verified)
    
#     def test_login(self):
#         url = reverse('verify-email', kwargs={'verification_token': self.user.verification_token})
#         self.client.get(url)
#         url = reverse('login')
#         data = {'email': 'user3@example.com', 'password': 'password123'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)
#         token = Token.objects.get(user=self.user)
#         self.assertEqual(response.data['token'], token.key)
    
#     def test_logout(self):
#         self.client.force_authenticate(user=self.user)
#         url = reverse('logout')
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_change_password(self):
#         self.client.force_authenticate(user=self.user)
#         url = reverse('change-password')
#         data = {'old_password': 'password123', 'new_password': 'newpassword123', 'confirm_password':'newpassword123'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('newpassword123'))

