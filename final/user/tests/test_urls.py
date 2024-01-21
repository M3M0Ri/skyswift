from django.test import TestCase
from user.views import UserSignUp, Login, Logout, ChargingAccount
from django.urls import reverse, resolve


class TestUrls(TestCase):
    def test_signup(self):
        url = reverse("user:signup")
        self.assertEquals(resolve(url).func.view_class, UserSignUp)

    def test_login(self):
        url = reverse("user:login")
        self.assertEquals(resolve(url).func.view_class, Login)

    def test_logout(self):
        url = reverse("user:logout")
        self.assertEquals(resolve(url).func.view_class, Logout)

    def test_charge_account(self):
        url = reverse("user:charging_account")
        self.assertEquals(resolve(url).func.view_class, ChargingAccount)


