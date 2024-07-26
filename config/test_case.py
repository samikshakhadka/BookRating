#from django.contrib.auth import get_user_model
import uuid
from django.test import override_settings
from apps.user.models import CustomUser
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.user.tests.factories import UserFactory
from apps.book.tests.factories import BookFactory ,FavoriteFactory


class ApiTestMixin:
    client_class = APIClient()

    def authenticate(self,user=None):
        if user is None:
            unique_email = f'{uuid.uuid4()}@example.com'
            user = CustomUser.objects.create_user(email=unique_email, password='password123')
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return token
            # create token and set the credential for the user in the header



@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True
)
class ApiTestCase(APITestCase, ApiTestMixin):


    
    def setUp(self):
        
        self.super_user = UserFactory(is_superuser=True, is_staff=True, password='password@123')
        #self.user = UserFactory()
        self.user = UserFactory(password='Apassword@123', is_verified=True)
        self.book = BookFactory(created_by=self.user)
        self.client = APIClient()
        super().setUp() 
        
    
    @classmethod
    def create_user(cls):
        user = UserFactory()
        user.set_password('Apassword@123')  # Set the password used for login
    
        user.save()
        return user