from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings
from django.urls import reverse


class LoginViewTest(TestCase):
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