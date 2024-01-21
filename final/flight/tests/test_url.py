from django.test import TestCase
from django.urls import reverse, resolve
from flight.views import *


class TestFlightUrl(TestCase):
    def test_root_url(self):
        url = reverse('flight:feed') #/
        self.assertEqual(resolve(url).func.view_class, index)

    def test_all_flights_url(self):
        url = reverse('flight:flight_list')
        self.assertEqual(resolve(url).func.view_class, FlightListView)

    def test_search_flights_by_date_url(self):
        url = reverse('flight:search_flight_by_date')
        self.assertEqual(resolve(url).func.view_class, search_flights_byDate)

