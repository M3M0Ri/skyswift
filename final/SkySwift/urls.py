from django.contrib import admin
from django.urls import path, include
from flight.views import index
urlpatterns = [
    path("" , index , name="main page"),
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('ticket/', include('ticket.urls')),
    path('flight/', include('flight.urls')),
]
