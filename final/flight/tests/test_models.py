from django.test import TestCase
from flight.models import *


class TestAirportModel(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(
            name= "MehrAbad",
            country= "Iran",
            city="Tehran"
        )

    def test_creates_airport(self):
        self.assertEqual(self.airport.name, "MehrAbad")
        self.assertEqual(self.airport.country, "Iran")
        self.assertEqual(self.airport.city, "Tehran")

    def test_airport_model_str(self):
        airport_str = str(self.airport) # from docu -> str means __str__
        self.assertEqual(airport_str, "MehrAbad-Iran-Tehran")
