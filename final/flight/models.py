from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .countries import countries
from .manager import FlightManger, AirPortManger, AirplaneManger

formatted_countries = [(country["code"], country["name"]) for country in countries]




class Airport(models.Model):
    name = models.CharField(max_length=55, default="")
    # country = models.CharField(max_length=50, choices=formatted_countries, default='')
    country = models.CharField(max_length=50, choices=formatted_countries, default='')
    city = models.CharField(max_length=30, default='')

    objects = models.Manager()
    airports = AirPortManger()

    def __str__(self):
        return f"{self.name}-{self.city}-{self.country}"

    def to_json(self):
        return {
            'name': self.name,
            'city': self.city,
            'country': self.country,
        }


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    departure = models.DateTimeField(default=datetime.now)
    arrival = models.DateTimeField(default=datetime.now)
    price = models.PositiveIntegerField(default=0, blank=False)
    cost_of_cancel = models.PositiveIntegerField(default=0, blank=True,
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    airplane = models.ForeignKey('Airplane', on_delete=models.SET_NULL, null=True, related_name="flights", blank=True)
    unique_id = models.CharField(max_length=200, default=f"", blank=True)
    capacity = models.PositiveIntegerField(default=40, validators=[MinValueValidator(1), MaxValueValidator(100)])
    count_of_reserved = models.PositiveIntegerField(default=0)

    flights = FlightManger()
    objects = models.Manager()

    def __str__(self):
        return f"A flight from {self.origin} to {self.destination},  airplane : {self.airplane} , price : {self.price}"

    def get_passengers(self):
        # Get all passengers for this flight
        from ticket.models import Ticket
        passengers = Ticket.objects.filter(flight=self).values('user').distinct()

        # Map each passenger to their corresponding user
        mapped_passengers = {passenger['user']: passenger for passenger in passengers}

        return mapped_passengers

    def save(self, *args, **kwargs):
        # Set the value of the private field before saving
        self.capacity = self.airplane.capacity
        self.unique_id = f"{self.origin}-{self.destination}-{self.departure.strftime('%Y:%m:%d (%H:%M)')}-{self.arrival.strftime('%Y:%m:%d (%H:%M)')}"

        # Call the actual save method to save the instance
        super(Flight, self).save(*args, **kwargs)

    def get_available_seats(self):
        return self.capacity - self.count_of_reserved


class Airplane(models.Model):
    brand = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50, default="")
    company_name = models.CharField(max_length=60, default="")
    capacity = models.PositiveIntegerField(default=40, validators=[MinValueValidator(1), MaxValueValidator(100)])

    airplans = AirplaneManger()
    objects = models.Manager()

    def __str__(self):
        return f"{self.brand}-{self.model}-{self.company_name}"
