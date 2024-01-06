from django.urls import path

from .views import create_ticket, list_tickets, buying_ticket_page, cancelTicket, list_record_of_tickets

app_name = "ticket"
urlpatterns = [
    path('create/', create_ticket, name="creating_ticket"),
    path('all/', list_tickets, name="list_of_all_ticket_for_user"),
    path('buy/<int:fpk>/', buying_ticket_page.as_view(), name='buying_ticket'),
    path("cancel/<int:tpk>/", cancelTicket.as_view(), name="cancel_ticket"),
    path("record/", list_record_of_tickets, name="record_of_tickets")
]
