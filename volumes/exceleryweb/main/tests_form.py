from .forms import SignupForm
from django.test import TestCase
from django.contrib.auth.models import User


class TestSignupForm(TestCase):

    def setUp(self):
        User.objects.create(username='user1', password='test')
    
    def test_form_valid_data(self):
        form = SignupForm({
            'username': 'user3',
            'password': 'test',
            're_password': 'test',
            'accept_rules': True
        })
        self.assertTrue(form.is_valid())
    
    def test_form_password_match(self):
        form = SignupForm({
            'username': 'user3',
            'password': 'test',
            're_password': 'teste',
            'accept_rules': True
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password error', form.errors['__all__'])
    
    def test_accept_rules(self):
        form = SignupForm({
            'username': 'user3',
            'password': 'test',
            're_password': 'test',
            'accept_rules': False
        })
        self.assertFalse(form.is_valid())
        self.assertIn('لطفا قوانین رو قبول کنید', form.errors['accept_rules'])

    def test_unique_username(self):
        form = SignupForm({
            'username': 'user1',
            'password': 'test',
            're_password': 'test',
            'accept_rules': False
        })
        self.assertFalse(form.is_valid())
        self.assertIn('یوزرنیم تکراری است', form.errors['username'])