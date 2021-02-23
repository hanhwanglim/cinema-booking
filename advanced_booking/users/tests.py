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
        The login functionality should login the user with the correct credentials.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Create test user
        test_user_email = 'user1@user1.com'
        test_user_name = 'user1'
        test_user_password = 'password123'
        user = User.objects.create(
            email=test_user_email, 
            username=test_user_name, 
        )
        user.set_password(test_user_password)
        user.save()

        # Test when user keys in wrong password
        is_logged_in = self.client.login(email=test_user_email, password='wrongpassword')
        self.assertFalse(is_logged_in)

        # Test when user keys in wrong email
        is_logged_in = self.client.login(email='wrongemail@email.com', password=test_user_password)
        self.assertFalse(is_logged_in)
        
        # Test when user keys in right information
        is_logged_in = self.client.login(email=test_user_email, password=test_user_password)
        self.assertTrue(is_logged_in)


    def test_register_users(self):
        """
        The register page should create a new user in the database.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        test_user_email = 'user1@user1.com'
        test_user_username = 'user1'
        test_user_password = 'Qzh6=?sx-!B-eeJ6'
        test_user_birthday = date(2010, 1, 1)
        form = {
            'email': test_user_email, 
            'username': test_user_username,
            'password1': test_user_password,
            'password2': test_user_password,
            'birthday': test_user_birthday,
            'accept_tos': True,
        }
        response = self.client.post('/register', form, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email=test_user_email)
        self.assertEqual(user.email, test_user_email)
        self.assertEqual(user.username, test_user_username)
        self.assertEqual(user.birthday, test_user_birthday)
        
        # Password cannot be asserted as it is hashed.
        # Testing for password is done by using login instead.
        is_logged_in = self.client.login(email=test_user_email, password=test_user_password)
        self.assertTrue(is_logged_in)

