from django.test import TestCase
from django.contrib.auth.models import User as DjangoUser
from .models import User

class UserModelTest(TestCase):

    def setUp(self):
        """Create a Django user and corresponding custom user for testing."""
        self.django_user = DjangoUser.objects.create_user(
            username='testuser',
            password='password123',
        )
        self.user = User.objects.create(
            user=self.django_user,
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='password123',
        )

    def test_user_creation(self):
        """Test if a User instance is created correctly."""
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.com')

    def test_user_str(self):
        """Test if the __str__ method works correctly."""
        self.assertEqual(str(self.user), 'John Doe (johndoe@example.com)')

    def test_user_email_uniqueness(self):
        """Test that the email field must be unique."""
        with self.assertRaises(Exception):
            User.objects.create(
                user=self.django_user,
                first_name='Jane',
                last_name='Smith',
                email='johndoe@example.com',  
                password='password456',
            )

    def test_required_fields(self):
        """Test that required fields are respected when creating a User."""
        with self.assertRaises(Exception):
            User.objects.create(
                user=self.django_user,
                first_name='Jane',
                last_name='Smith',
                email='janesmith@example.com'
               
            )

    def test_update_user_details(self):
        """Test that a user's details can be updated."""
        self.user.first_name = 'Jane'
        self.user.save()
        self.assertEqual(self.user.first_name, 'Jane')

