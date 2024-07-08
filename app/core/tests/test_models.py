"""
Tests for the models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "testpass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testpass123")

    def test_create_superuser(self):
        """Test creating a new superuser."""
        email = "superuser@example.com"
        user = get_user_model().objects.create_superuser(
            email=email,
            password="superpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_with_extra_fields(self):
        """Test creating a user with extra fields is successful."""
        email = "test@example.com"
        password = "testpass123"
        first_name = "Test"
        last_name = "User"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)


