from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError
from django.db import transaction
from django.urls import reverse
import json


class UserNameSaveTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
                    username = "yantre",
                    email ="ayogesh@terafastnet.com",
                    
                    is_staff = True,
                    )
        self.user.set_password("123456")

    def test_00_check_if_username_saved(self):
        #setup would have already created an username, check if the username is what we set
        userUrl = "http://127.0.0.1:8000/auth/login/"
        response = self.client.get(userUrl)
        users = response.json()
        #print(users[0])
        #verify we have one user created.
        self.assertEqual(users[0]["username"], "yantre")

# Import necessary modules
from django.test import TestCase
from django.contrib.auth.models import User

# Define your test case class
class UserModelTest(TestCase):

    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass123'
        )

    def test_user_creation(self):
        # Test user was created correctly
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_user_password(self):
        # Test user password is set correctly (passwords are hashed in Django)
        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str(self):
        # Test string representation of the user (this usually returns the username)
        user = User.objects.get(username='testuser')
        self.assertEqual(str(user), 'testuser')

    def test_user_authentication(self):
        # Test if the user can authenticate with correct credentials
        user = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(user)

    def test_user_authentication_fail(self):
        # Test if the user authentication fails with incorrect credentials
        user = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(user)


        