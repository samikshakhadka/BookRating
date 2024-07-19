from django.contrib.auth import get_user_model
from django.test import TestCase
from uuid import UUID

User = get_user_model()

class CustomUserModelTest(TestCase):
    
    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertIsInstance(user.verification_token, UUID)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', password='adminpassword123')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
