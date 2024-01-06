import logging

import mailtrap as mt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from django.views.generic import ListView

from flight.models import Flight
from ticket.forms import TicketForm
from user.models import MyUserModel
from .forms import CreditCardForm
from .models import Ticket
from django.core.mail import send_mail
from django.core.mail import EmailMessage
log = logging.getLogger(__name__)


def send_welcome_email(user_email, ticket_messsage):
    print(user_email , "    ---- ", ticket_messsage)
    subject = 'Buying ticket Success'
    message = ticket_messsage
    from_email = 'resolver@skyswift.com'
    recipient_list = user_email
    msg = EmailMessage(subject,
                       message, to=[from_email])
    msg.send()
    log.info(f"message send : {msg.subject}")


@login_required(login_url="http://localhost:8000/user/login/")
def create_ticket(request):
    try:
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                form.save()
                log.info(f"ticket saved -> {form.id}")
                return redirect('list_of_all_ticket')
        else:
            form = TicketForm()

    except Exception as e:
        log.error(str(e))
    context = {'form': form}
    return render(request, 'tickets/create.html', context)


@login_required(login_url="http://localhost:8000/user/login/")
def list_tickets(request):
    requested_user = request.user.id
    tickets = Ticket.objects.filter(Q(user=requested_user), active=True)
    context = {'tickets': tickets}
    return render(request, 'tickets/ticket_list.html', context)


def list_record_of_tickets(request):
    requested_user = request.user.id
    tickets = Ticket.objects.filter(Q(user=requested_user))
    context = {'tickets': tickets}
    return render(request, 'tickets/ticket_record.html', context)


class FlightDoesNotExist:
    pass


class cancelTicket(LoginRequiredMixin, View):
    login_url = "http://localhost:8000/user/login/"

    def get(self, request, *args, **kwargs):
        ticket_key = kwargs["tpk"]
        print(Ticket.objects.get(pk=ticket_key))
        ticket = Ticket.objects.get(pk=ticket_key)
        user = MyUserModel.objects.get(pk=request.user.id)
        flight = Flight.objects.get(pk=ticket.flight_id)
        user.charge = int(user.charge) + (
                int(ticket.price) - (int(ticket.price) * ((100 - int(flight.cost_of_cancel)) / 100)))
        ticket.active = False
        user.save()
        ticket.save()
        return redirect("flight:feed")


class buying_ticket_page(ListView, View):
    template_name = 'tickets/buying.html'
    login_url = "user:sign-in"

    def get(self, request, *args, **kwargs):
        flight_pk = kwargs["fpk"]
        print(request.user.username, "This is the username of user")
        template = loader.get_template(self.template_name)
        try:
            flight = Flight.objects.get(pk=flight_pk)
            if flight:
                credit_card_form = CreditCardForm()
                return HttpResponse(template.render({'flight': flight, "forms": credit_card_form}, request))
            else:
                return HttpResponse("404 , not found")
        except ObjectDoesNotExist:
            return HttpResponse("404 , not found")

    def post(self, request, *args, **kwargs):
        global credit_card_value
        credit_card = {
            "cc_number": request.POST.get("credit_card_number"),
            "credit_card_holder_name": request.POST.get("credit_card_holder_name"),
            "expiration_year": request.POST.get("expiration_year"),
            "expiration_month": request.POST.get("expiration_month"),
            'cvv': request.POST.get("cvv")
        }
        try:
            credit_card_value = CreditCardForm(request.POST)
            person_pk = request.user.id
            if credit_card_value.is_valid() and person_pk:
                user = MyUserModel.objects.get(pk=person_pk)  # check later
                flight = Flight.objects.get(pk=kwargs["fpk"])
                result = Ticket.objects.create(user=user, flight=flight, price=60,
                                               seat_number=flight.count_of_reserved + 1)
                flight.count_of_reserved = flight.count_of_reserved + 1
                flight.save()
                send_welcome_email(user.email , result.__str__())
                log.info(f"flight {flight.id} saved")
                return render(request, 'tickets/success.html', {'ticket': result})
        except Exception as e:
            form_errors = credit_card_value.errors
            print(form_errors)
            template = loader.get_template('tickets/buying.html')
            return HttpResponse(template.render(
                {'flight': Flight.objects.get(pk=kwargs["fpk"]), "forms": credit_card_value,
                 'form_errors': form_errors}, request))
