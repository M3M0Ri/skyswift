from django.urls import path

from user.views import UserSignUp, Logout, Login, ChargingAccount

app_name = "user"

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name="signup"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('charge/', ChargingAccount.as_view(), name="charging_account")
]
