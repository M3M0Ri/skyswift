from django.test import TestCase, Client
from django.urls import reverse
from user.models import MyUserModel, Profile


class TestUserSignUp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_signup_GET(self):
        response = self.client.get(reverse("user:signup"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "authoriziation/signup.html")



