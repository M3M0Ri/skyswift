from django.db.models import Manager

import flight.models


class FlightManger(Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def get_available_flights(self):
        return self.filter(count_of_reserved__lt=flight.models.Flight)

    def get_flight_id(self, id):
        return super().get_queryset().filter(unique_id=id)

    def get_most_expensive_flight(self):
        return self.order_by('-price').first()

    def get_cheapest_flight(self):
        return self.order_by('price').first()

    def get_flights_with_available_seats(self, destination=None, max_seats=None):
        flights = super().get_queryset().filter(capacity__gt=flight.models.Flight.count_of_reserved)
        if destination:
            flights = flights.filter(destination=destination)

        if max_seats:
            flights = flights.filter(capacity__gt=max_seats - flight.models.Flight.count_of_reserved)

        return flights


class AirPortManger(Manager):
    def get_by_name_and_country(self, name, country):
        return self.filter(name=name, country=country).first()

    def get_by_city(self, city):
        return self.filter(city=city).all()


class AirplaneManger(Manager):
    def get_airplanes_by_company_name(self, company_name):
        return self.filter(company_name=company_name)

    def get_airplanes_by_capacity(self, min_capacity, max_capacity):
        return self.filter(capacity__gte=min_capacity, capacity__lte=max_capacity)

