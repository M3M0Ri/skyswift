from django.urls import path

from flight import views

app_name = "flight"

urlpatterns = [
    path('', views.index, name='feed'),
    path("all/", views.FlightListView.as_view(), name="all_flights"),
    path('flightlist/', views.all_flight.as_view(), name="flight_list"),
    path("search/", views.search_flights, name="search_flight"),
    path('detail/<int:flight_id>', views.FlightView.as_view(), name="each_flight_page"),
    path("create/", views.FlightCreateView.as_view(), name="create_flight"),
    path("user_tickets/", views.user_tickets, name="user_tickets"),
    path("create/airport/", views.create_airport, name="create_airport"),
    path('search/date/', views.search_flights_byDate, name="search_flight_by_date")
]
