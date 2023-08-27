from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    def setUp(self):
        self.username = 'test'
        self.email = 'test@example.com'
        self.password = 'test@123'

    def test_create_user(self):
        """Test to create user successfully. """
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)

        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)

    def test_email_normalized_for_user(self):
        """ Test to check email normailization. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMple.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, outcome in sample_emails:
            user = get_user_model().objects.create_user(
                username=self.username,
                email=email,
                password=self.password)
            self.assertEqual(user.email, outcome)

    def test_create_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
