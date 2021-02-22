from datetime import date

from django.urls import reverse
from django.test import TestCase

from .models import User


def create_user(email, username, password):
    """
    Create a new user with the given email, username and password.
    """
    return User.objects.create(
        email=email,
        username=username,
        password=password
    )


class LoginViewTest(TestCase):
    def test_user_login(self):
        """
        The login page should redirect onto the home page if the user has
        logged on
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Create test user
        test_user_email = 'user1@user1.com'
        test_user_name = 'user1'
        test_user_password = 'password123'
        create_user(test_user_email, test_user_name, test_user_password)

        # Test when user keys in wrong information
        wrong_login_form = {
            'email': test_user_email,
            'password': 'wrongpassword',
            'remember': 'false'
        }
        response = self.client.post(reverse('login'), wrong_login_form, follow=True)
        self.assertEqual(response.status_code, 200)
        # TODO: assert error messages in the login page
        
        # Test when user keys in right information
        correct_login_form = {
            'email': test_user_email,
            'password': test_user_password,
            'remember': 'false'
        }
        response = self.client.post(reverse('login'), correct_login_form, follow=True)
        self.assertEqual(response.status_code, 200)
        # TODO: assert redirected to page after login
