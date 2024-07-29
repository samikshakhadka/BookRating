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
from unittest.mock import patch

class UserRegistrationTests(ApiTestCase):

    def setUp(self):
        self.url = '/user/register/'
        self.base_data = {
            'email': 'newuser@example.com',
            'password': 'Apassword@123',
            'first_name': 'New',
            'last_name': 'User'
        }

    def get_response(self, data):
        return self.client.post(self.url, data, format='json')

    def test_register(self):
        """
        Test registering a user with valid data.
        """
        response = self.get_response(self.base_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.base_data['email'])

    
        """
        Test registering a user with an already existing email.
        """
        user = UserFactory(email='existing@example.com')
        data = self.base_data.copy()
        data['email'] = user.email
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'A user with that email already exists.')

    
        """
        Test registering a user with an invalid email.
        """
        data = self.base_data.copy()
        data['email'] = 'invalid-email'
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
        """
        Test registering a user with a password that is too short.
        """
        data = self.base_data.copy()
        data['password'] = 'short'
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
        """
        Test registering a user without providing a password.
        """
        data = self.base_data.copy()
        del data['password']
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    
        """
        Test registering a user without providing an email.
        """
        data = self.base_data.copy()
        del data['email']
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserEmailVerificationTests(ApiTestCase):

    @patch('apps.user.tasks.send_verification_email_task.delay') #remove delay
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


    def test_verify_email_with_invalid_token(self):
        '''
        Test verifying email with an invalid token.
        '''
        user = UserFactory(is_verified=False)
        token = "ygbuhbjhbjh"      
        url = f'/user/verify-email/{str(token)}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)
        user.refresh_from_db()
        self.assertFalse(user.is_verified)


class UserLoginTests(ApiTestCase):
 
    def test_login(self):
        '''
        Test logging in with valid credentials.
        '''
       
        user = UserFactory(is_verified=True, password = 'Apassword@123') #use passwprd in factory
        url = '/user/login/'
        data = {
            'email': user.email,
            'password': 'Apassword@123'# This should match the password set in create_user
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])

        '''
        Test logging in with invalid credentials.
        '''
        user = UserFactory(is_verified=False, password = 'Apassword@123')
        url = '/user/login/'
        data = {
            'email': user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

   
        '''
        Test logging in with an unverified email.
        '''
        url = '/user/login/'
        user = UserFactory(is_verified=False, password = 'Apassword@123')
        data = {
            'email': user.email,
            'password': 'Apassword@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        self.assertEqual(
        str(response.data['non_field_errors'][0]),
        'Email not verified. Please check your email to verify your account.'
        )


     
class ChangePasswordTests(ApiTestCase):
    
    def setUp(self):
        self.url = '/user/change-password/'
        self.user = UserFactory(is_verified=True, password='Apassword@123')
        self.client.force_authenticate(user=self.user)
        self.base_data = {
            'old_password': 'Apassword@123',
            'new_password': 'Anewpassword@123',
            'confirm_password': 'Anewpassword@123'
        }

    def get_response(self, data):
        return self.client.post(self.url, data, format='json')

    def test_change_password_(self):
        """
        Test changing the password with valid data.
        """
        response = self.get_response(self.base_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
        """
        Test changing the password with an invalid old password.
        """
        data = self.base_data.copy()
        data['old_password'] = 'wrongpassword'
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
        """
        Test changing the password with mismatched new and confirm passwords.
        """
        data = self.base_data.copy()
        data['new_password'] = 'newpassword123'
        data['confirm_password'] = 'differentpassword'
        response = self.get_response(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



















# class UserRegistrationTests(ApiTestCase):


#     def test_register(self):
#         '''
#         Test registering a user with valid data.
#         '''
#         url = '/user/register/'
#         data = {
#             'email': 'newuser@example.com',
#             'password': 'Apassword@123',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['email'],data['email'])

#         # Testing with already exist email
#         user = UserFactory(email='existing@example.com')
#         data = {
#             'email': user.email,
#             'password': 'Apassword@123',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['email'][0], 'A user with that email already exists.')


    
#         '''
#         Test registering a user with an invalid email.
#         '''
#         url ='/user/register/'
#         data = {
#             'email': 'invalid-email',
#             'password': 'password123',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    
#         '''
#         Test registering a user with a password that is too short.
#         '''
#         url = '/user/register/'
#         data = {
#             'email': 'newuser@example.com',
#             'password': 'short',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    
#         '''
#         Test registering a user without providing a password.
#         '''
#         url = '/user/register/'
#         data = {
#             'email': 'newuser@example.com',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('password', response.data)

    
#         '''
#         Test registering a user without providing an email.
#         '''
#         url = '/user/register/'
#         data = {
#             'password': 'password123',
#             'first_name': 'New',
#             'last_name': 'User'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)


#class ChangePasswordTests(ApiTestCase):
    # def test_change_password(self):
    #     '''
    #     Test changing the password with valid data.
    #     '''
    #     url = '/user/change-password/'
    #     user = UserFactory(is_verified=True, password = 'Apassword@123') 
           
    #     data = {
    #         'old_password': 'Apassword@123',
    #         'new_password': 'Anewpassword@123',
    #         'confirm_password': 'Anewpassword@123'
    #     }
    #     self.client.force_authenticate(user=user)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        
    #     # invalid or old password

    #     # data['old_password'] = 'wrongpassword'
    #     # response = self.client.post(url, data, format='json')
    #     # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     data = {
    #         'old_password': 'wrongpassword',
    #         'new_password': 'Anewpassword@123',
    #         'confirm_password': 'Anewpassword@123'
    #     } 
    #     self.client.force_authenticate(user=user)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
          

    #     #mismatched new password
    #     data = {
    #         'old_password': 'Apassword@123',
    #         'new_password': 'newpassword123',
    #         'confirm_password': 'differentpassword'
    #     }
    #     self.client.force_authenticate(user=user)
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        





























 