from datetime import date

from django.urls import reverse
from django.test import TestCase

from .models import User


class LoginViewTest(TestCase):
    def test_login_page(self):
        """
        The login page should have a form that allows users to login into.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

