from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings
from django.urls import reverse


class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='admin1381_08_321fortest', password='admin')
    
    def test_login_page_status_code(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_address_in_settings(self):
        response = self.client.get(settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_page_template_used(self):
        response = self.client.get(reverse('main:login'))
        self.assertTemplateUsed(response, 'main/auth.html')
    
    def test_login_successful(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'admin1381_08_321fortest',
            'password': 'admin'
        })
        self.assertRedirects(response, reverse('main:home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_unsuccessful(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'wrongUsername',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'نام کاربری اشتباه است')
    
    def test_redirect_authenticated_user(self):
        self.client.login(username='admin1381_08_321fortest', password='admin')
        response = self.client.get(reverse('main:login'))
        self.assertRedirects(response, reverse('main:home'))


class TestSignupView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='user1', password='test')
        
    def test_status_code(self):
        response = self.client.get(reverse('main:signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('main:signup'))
        self.assertTemplateUsed(response, 'main/auth.html')
    
    def test_signup_successful_new_user(self):
        response = self.client.post(reverse('main:signup'), {
            'username': 'user2',
            'password': 'test',
            're_password': 'test',
            'accept_rules': True
        })
        self.assertRedirects(response, reverse('main:home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'user2')
    
    def test_unique_username_not_doplicat_password(self):
        response = self.client.post(reverse('main:signup'), {
            'username': 'user1',
            'password': 'test',
            're_password': 'test2',
            'accept_rules': True
        })
        self.assertContains(response, 'یوزرنیم تکراری است')
        # self.assertFormError(response=response, form='form', field='username', errors=['یوزرنیم تکراری است'])
        self.assertContains(response, 'رمز عبور و تکرار ان با هم برابر نیستند.')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_signup_failure_with_not_accept_rules(self):
        response = self.client.post(reverse('main:signup'), {
            'username': 'user3',
            'password': 'test',
            're_password': 'test',
            'accept_rules': False
        })
        self.assertContains(response, 'لطفا قوانین رو قبول کنید')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIn('form', response.context)
        self.assertTrue('form', response.context['form'].is_bound)


class TestLogout(TestCase):
    def setUp(self):
        User.objects.create_user(username='user1', password='test')
    
    def test_logout_successful(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'user1',
            'password': 'test'
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)