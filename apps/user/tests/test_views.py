from django.urls import path, include
from rest_framework import status
from config.test_case import ApiTestCase
from apps.user.models import CustomUser
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.user.tests.factories import UserFactory
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class UserRegistrationTests(ApiTestCase):


    def test_register_user_with_valid_data(self):
        '''
        Test registering a user with valid data.
        '''
        url = '/user/register/'
        data = {
            'email': 'newuser@example.com',
            'password': 'Apassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'],data['email'])

        # Testing with already exist email
        user = UserFactory(email='existing@example.com')
        user.save()
        data = {
            'email': user.email,
            'password': 'Apassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'A user with that email already exists.')


    # def test_register_user_with_existing_email(self):
    #     '''
    #     Test registering a user with an email that already exists.
    #     '''
    #     user = UserFactory(email='existing@example.com')
    #     user.save()
    #     url='/user/register/'
    #     data = {
    #         'email': user.email,
    #         'password': 'Apassword123',
    #         'first_name': 'New',
    #         'last_name': 'User'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['email'],data['email'])

    def test_register_user_with_invalid_email(self):
        '''
        Test registering a user with an invalid email.
        '''
        url ='/user/register/'
        data = {
            'email': 'invalid-email',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_user_with_short_password(self):
        '''
        Test registering a user with a password that is too short.
        '''
        url = '/user/register/'
        data = {
            'email': 'newuser@example.com',
            'password': 'short',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_user_without_password(self):
        '''
        Test registering a user without providing a password.
        '''
        url = '/user/register/'
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_user_without_email(self):
        '''
        Test registering a user without providing an email.
        '''
        url = '/user/register/'
        data = {
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

from unittest.mock import patch
from django.urls import reverse

class UserEmailVerificationTests(ApiTestCase):


    @patch('apps.user.tasks.send_verification_email_task.delay')
    def test_verify_email_with_valid_token(self, mock_send_verification_email):
        '''
        Test verifying email with a valid token and mock sending email task.
        '''
        user = UserFactory(is_verified=False)
        url = f'/user/verify-email/{user.verification_token}/'

        # Trigger the email verification process
        response = self.client.get(url, format='json')

        # Check response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh user data and check if user is verified
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

        
        





    # def test_verify_email_with_valid_token(self):
    #     '''
    #     Test verifying email with a valid token.
    #     '''
    #     user = UserFactory(is_verified=False)

    #     url = f'/user/verify-email/{user.verification_token}/'
    #     print(f'Testing URL1: {url}')
    #     response = self.client.get(url, format='json')
    #     print(f'Response status code1: {response.status_code}')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     user.refresh_from_db()
    #     self.assertTrue(user.is_verified)

    # def test_verify_email_with_invalid_token(self):
    #     '''
    #     Test verifying email with an invalid token.
    #     '''
    #     user = UserFactory(is_verified=False)
    #     print("token type", type(user.verification_token))
    #     token = "ygbuhbjhbjh"
    #     print("******************token", token)

    #     url = f'/user/verify-email/{str(token)}/'
    #     print(f'Testing URL: {url}')
    #     #url = f'/user/verify-email/{invalid_token}/'
    #     response = self.client.get(url, format='json')
    #     print('Response status code', response)
    #     self.assertEqual(response.status_code, 404)
    #     user.refresh_from_db()
    #     self.assertFalse(user.is_verified)


class UserLoginTests(ApiTestCase):
    # def setUp(self):
    #     super().setUp()
    #     # Create a user to test registration with existing email
    #     self.user = CustomUser.objects.create_user(
    #         email='existing@example.com',
            
    #     )

    
    def test_login_with_valid_credentials(self):
        '''
        Test logging in with valid credentials.
        '''
        #url = '/user/login/'
        # data = {
        #     'email': self.user.email,
        #     'password': 'Apassword123'
        # }
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('token', response.data)

        # user = self.create_user()
        # user.is_verified = True
        # user.save()
        # print("5555555555555555555555555555555555", user.password)
        # print("************************************", user.email)
        # url = '/user/login/'
        # data = {
        #     'email': user.email,
        #     'password': 'Apassword@123'# This should match the password set in create_user
        # }
        # response = self.client.post(url, data, format='json')
        # # print("################", response.json())
        # self.assertEqual(response.status_code, 200)
        # self.assertIsNotNone(response.data['token'])

        #user = self.create_user()
        user = UserFactory(is_verified=True)
        #user.is_verified = True
        user.set_password('Apassword@123')
        user.save()
        url = '/user/login/'
        data = {
            'email': user.email,
            'password': 'Apassword@123'# This should match the password set in create_user
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])




    def test_login_with_invalid_credentials(self):
        '''
        Test logging in with invalid credentials.
        '''
        user = UserFactory(is_verified=False)
        #user = self.create_user()
        #user.is_verified = True
        #user.set_password('password123')
        #user.save()
        url = '/user/login/'
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_login_with_unverified_email(self):
        '''
        Test logging in with an unverified email.
        '''
        url = '/user/login/'
        user = UserFactory(is_verified=False)
        user.set_password('password123')
        user.save()
        data = {
            'email': user.email,
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        #self.assertEqual(response.data['non_field_errors'][0], ErrorDetail('Email not verified. Please check your email to verify your account.', code='invalid'))
        self.assertEqual(
        str(response.data['non_field_errors'][0]),
        'Email not verified. Please check your email to verify your account.'
        )
class ChangePasswordTests(ApiTestCase):
    # def setUp(self):
    #     super().setUp()
    #     self.token = Token.objects.create(user=self.user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_change_password(self):
        '''
        Test changing the password with valid data.
        '''
        url = '/user/change-password/'
        user = UserFactory(is_verified=True)
        user.set_password('Apassword@123')
        user.save()

        self.authenticate(user=user)
        data = {
            'old_password': 'Apassword@123',
            'new_password': 'Anewpassword@123',
            'confirm_password': 'Anewpassword@123'
        }
        self.authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('Anewpassword@123'))

        # invalid or old password

        data = {
            'old_password': 'wrongpassword',
            'new_password': 'Anewpassword@123',
            'confirm_password': 'Anewpassword@123'
        }
        self.authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
          # true or false

        #mismatched new password
        data = {
            'old_password': 'Apassword@123',
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword'
        }
        self.authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #check asser passwrd or not

    # def test_change_password_with_invalid_old_password(self):
    #     '''
    #     Test changing the password with an invalid old password.
    #     '''
    #     url = '/user/change-password/'
    #     user = UserFactory(is_verified=True)
    #     user.set_password('Apassword@123')
    #     user.save()
    #     data = {
    #         'old_password': 'wrongpassword',
    #         'new_password': 'Anewpassword@123',
    #         'confirm_password': 'Anewpassword@123'
    #     }
    #     self.authenticate(user=user)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     user.refresh_from_db()
    #     self.assertTrue(user.check_password('Apassword@123'))

    # def test_change_password_with_mismatched_new_passwords(self):
    #     '''
    #     Test changing the password with mismatched new passwords.
    #     '''
    #     url = '/user/change-password/'
    #     user = UserFactory(is_verified=True)
    #     user.set_password('Apassword@123')
    #     user.save()
    #     data = {
    #         'old_password': 'Apassword@123',
    #         'new_password': 'newpassword123',
    #         'confirm_password': 'differentpassword'
    #     }
    #     self.authenticate(user=user)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     user.refresh_from_db()
    #     self.assertTrue(user.check_password('password123'))


































# import uuid
# from django.urls import reverse
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.test import APIClient
# from unittest.mock import patch

# User = get_user_model()

# class RegisterViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('register')
#         self.user_data = {
#             'email': 'test@example.com',
#             'password': 'testpassword',
#             'first_name': 'Test',
#             'last_name': 'User'
#         }

#     @patch('apps.user.serializers.send_verification_email_task.delay')
#     def test_register_user(self, mock_send_verification_email_task):
#         response = self.client.post(self.url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(User.objects.filter(email='test@example.com').exists())
#         mock_send_verification_email_task.assert_called_once()

# class VerifyEmailTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             is_verified=False,
#             verification_token=uuid.uuid4()
#         )
#         self.url = reverse('verify-email', kwargs={'verification_token': self.user.verification_token})

#     def test_verify_email(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.is_verified)

# class LoginViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             is_verified=True
#         )
#         self.url = reverse('login')
#         self.login_data = {
#             'email': 'test@example.com',
#             'password': 'testpassword'
#         }

#     def test_login_user(self):
#         response = self.client.post(self.url, self.login_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)

# class LogoutViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             is_verified=True
#         )
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('logout')

#     def test_logout_user(self):
#         response = self.client.post(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
# class ChangePasswordViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             is_verified=True
#         )
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('change-password')
#         self.password_data = {
#             'old_password': 'testpassword',
#             'new_password': 'newpassword',
#             'confirm_password': 'newpassword'
#         }

#     def test_change_password(self):
#         response = self.client.post(self.url, self.password_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('newpassword'))





















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

