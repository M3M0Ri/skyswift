from django import forms

from .countries import countries
from .models import Flight, Airport, Airplane
from django.forms import ModelForm, CharField, ChoiceField
from .models import Airport


class FlightForm(forms.ModelForm):
    origin = forms.ModelChoiceField(queryset=Airport.objects.all(), label="origin")
    destination = forms.ModelChoiceField(queryset=Airport.objects.all(), label="destination")
    departure = forms.DateTimeField(label="departure")
    arrival = forms.DateTimeField(label="arrival")
    price = forms.IntegerField(min_value=0, label="price")
    cost_of_cancel = forms.IntegerField(min_value=0, label="cost_of_cancel")
    airplane = forms.ModelChoiceField(queryset=Airplane.objects.all(), label="airplane")

    class Meta:
        model = Flight
        fields = ("origin", "destination", "departure", "arrival", "price", "cost_of_cancel")
        widgets = {
            'departure': forms.DateTimeField(),
            'arrival': forms.DateTimeField()
        }


class AirportForm(forms.ModelForm):
    countries = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    class Meta:
        model = Airport
        fields = ['name', 'country', 'city']

