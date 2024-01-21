from django.test import TestCase
from ticket.models import Ticket
from user.models import *
from flight.models import *


class TestTicketModel(TestCase):
    def setUp(self):
        self.user = MyUserModel.objects.create_user(
            email='test@gmail.com',
            username='testuser',
            password='testpassword'
        )
        self.flight = Flight.objects.create(
            origin = "tabriz",
            destination = "tehran"
        )

        self.ticket = Ticket.objects.create(
            user=self.user,
            flight=self.flight,
            seat_number=10,
            price=2000

        )

    def test_creates_ticket(self):
        self.assertEqual(self.ticket.user, self.user)
        self.assertEqual(self.ticket.flight, self.flight)
        self.assertEqual(self.ticket.seat_number, 10)
        self.assertEqual(self.ticket.price, 2000)