import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from flight.models import Ticket
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from flight.forms import FlightForm
from flight.models import Flight, Airport, Airplane
from ticket.models import Ticket
from . import countries

log = logging.getLogger(__name__)


def index(request):
    print(request)
    print("show if user is authenticate", request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect("user:login")


def get_passengers_for_flight(flight_id):
    passengers = (
        Ticket.objects
        .filter(flight_id=flight_id)
        .values('user')
        .distinct()
    )

    return [passenger['user'] for passenger in passengers]


class FlightListView(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'flight/all_flights.html'
    # context_object_name = 'flights'
    login_url = "user:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flights = Flight.objects.all()

        flight_passenger_info = []
        available_seats = []
        for flight in flights:
            passengers = get_passengers_for_flight(flight.id)
            flight_passenger_info.append((flight, passengers))
            available_seats.append(flight.get_available_seats())
        context['flight_passenger_info'] = flight_passenger_info
        return context


class all_flight(LoginRequiredMixin, ListView):
    model = Flight
    template_name = 'flight/flight_list.html'
    context_object_name = 'flights'
    login_url = "user:sign-in"

    def get(self, request, *args, **kwargs):
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render({"flights": Flight.objects.all()}, request))


@login_required(login_url="user:login")
def search_flights(request):
    if request.method == "POST":
        try:
            city_origin = request.POST.get('cityOrigin')
            city_destination = request.POST.get('cityDestination')
            flights = Flight.objects.all()
            if city_destination and city_origin:
                flights = flights.filter(origin__city__contains=city_origin,
                                         destination__city__contains=city_destination)
            if city_origin:
                flights = flights.filter(origin__city__contains=city_origin)

            if city_destination:
                flights = flights.filter(destination__city__contains=city_destination)

            context = {"flights": flights}
            return render(request, 'flight/search.html', context)

        except Exception as e:
            log.error(f"search failed {str(e)}")
    return render(request, 'flight/search.html')


class FlightView(LoginRequiredMixin, View):
    login_url = "user:login"

    def get(self, request, flight_id):
        flight = get_object_or_404(Flight, pk=flight_id)
        return render(request, 'flight/flight.html', {'flight': flight})


class FlightCreateView(LoginRequiredMixin, FormView):
    model = Flight
    template_name = 'flight/createflight.html'
    form_class = FlightForm
    success_url = reverse_lazy('flight_list')
    login_url = "user:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airports'] = Airport.objects.all()
        context['airplanes'] = Airplane.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = FlightForm(request.POST)
        try:
            if form.is_valid():
                print(form.cleaned_data)
                flight = Flight(origin=form.cleaned_data.get("origin"),
                                destination=form.cleaned_data.get("destination"),
                                departure=form.cleaned_data.get("departure"),
                                arrival=form.cleaned_data.get("arrival"),
                                airplane=form.cleaned_data.get("airplane"),
                                cost_of_cancel=form.cleaned_data.get("cost_of_cancel"),
                                price=form.cleaned_data.get("price"))
                flight.save()
                log.info(f"saved flight -> {flight.id}")
                return redirect("flight_list")
            else:
                Airports = Airport.objects.all()
                airplanes = Airplane.objects.all()
                template = loader.get_template(self.template_name)
                return HttpResponse(
                    template.render(
                        {"airports": Airports, "airplanes": airplanes, "errors": form.errors},
                        request))
        except Exception as e:
            log.error(str(e))
            return redirect("flight:feed")

    def get(self, request, *args, **kwargs):
        print(request.user.role)
        if request.user.role == "agency":
            Airports = Airport.objects.all()
            airplanes = Airplane.objects.all()
            template = loader.get_template(self.template_name)
            return HttpResponse(
                template.render({"airports": Airports, "airplanes": airplanes}, request))
        else:
            return redirect("flight:feed")


def user_tickets(request):
    return redirect('list_of_all_ticket_for_user')


@login_required(login_url="user:login")
def create_airport(request):
    if request.user.role == "normal":
        return redirect("flight:feed")
    elif request.method == 'GET':
        return render(request, 'airport/create_airport.html', {"formatted_countries": countries})
    elif request.method == 'POST':
        print(request.POST)
        city = request.POST.get("city") or None
        country = request.POST.get("country") or None
        name = request.POST.get("name") or None
        if city and country and name:
            new_airport = Airport.objects.create(name=name, country=country, city=city)
            new_airport.save()
            return redirect('flight:feed')
        else:
            return render(request, 'airport/create_airport.html', {"formatted_countries": countries})


@login_required(login_url="user:login")
def search_flights_byDate(request):
    if request.method == "POST":
        try:
            startdate = request.POST.get('startdate')
            flights = Flight.objects.filter(departure__gte=startdate)
            context = {"flights": flights}
            return render(request, 'flight/search_flight_date.html', context)

        except Exception as e:
            log.error(f"search failed {str(e)}")
    return render(request, 'flight/search_flight_date.html')
