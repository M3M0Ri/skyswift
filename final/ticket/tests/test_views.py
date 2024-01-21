from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ticket.models import Ticket
from django.utils import timezone
from user.models import *
from flight.models import *


class TicketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUserModel.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_ticket_view(self):
        #self.client.login(username='testuser', password='testpassword')
        url = reverse('ticket:create_ticket')
        response = self.client.post(url, self.ticket_data, data={
            "origin": "tabriz",
            "destination": "tehran",
            "price": 34000,
            "departure": timezone.now() + timezone.timedelta(hours=2),
            "airplane": "A",
            "capacity" : 5

        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ticket.objects.filter(origin="tabriz", destination="tehran").exists())


