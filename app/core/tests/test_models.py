from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    def setUp(self):
        self.email = 'testing@example.com'
        self.password = 'testing@123'

    def test_create_user(self):
        """Test to create user successfully. """
        username = "test123"
        user = get_user_model().objects.create_user(
            username=username,
            email=self.email,
            password=self.password)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_email_normalized_for_user(self):
        """ Test to check email normailization. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMple.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        count = 1
        for email, outcome in sample_emails:
            user = get_user_model().objects.create_user(
                username=f'test{count}',
                email=email,
                password=self.password)
            self.assertEqual(user.email, outcome)
            count += 1

    def test_create_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            username="testing12",
            email="testing12@gmail.com",
            password=self.password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
