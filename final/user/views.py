import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .forms import ChargingAccountForm as bill
from .models import MyUserModel

log = logging.getLogger(__name__)


class UserSignUp(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("flight:feed")
        return render(req, "authoriziation/signup.html")

    def post(self, req):
        print(req.POST)
        try:
            if req.POST["role"] == "agency":
                email = req.POST["email"]
                password = req.POST["password"]
                user = MyUserModel.objects.create_user(
                    username=req.POST["username"],
                    email=req.POST["email"],
                    password=password,
                    fullname=req.POST["fullname"],
                    role=req.POST["role"]
                )
                user.save()
                user = MyUserModel.objects.latest("id")
                return doLogin(req, email, password)
            else:
                if req.POST["role"] == "normal":
                    email = req.POST["email"]
                    password = req.POST["password"]
                    user = MyUserModel.objects.create_user(
                        username=req.POST["username"],
                        email=req.POST["email"],
                        password=password,
                        fullname=req.POST["fullname"],
                        role=req.POST["role"]
                    )
                    user.save()
                    user = MyUserModel.objects.latest("id")
                    return doLogin(req, email, password)
        except Exception as e:
            message = str("Invalid Data")
            return render(req, "authoriziation/signup.html", {"message": message})


class Login(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("flight:feed")
        return render(req, "authoriziation/login.html", {})

    def post(self, req):
        email = req.POST["email"]
        password = req.POST["password"]
        return doLogin(req, email, password)


def doLogin(req, email, password):
    print("in login section to handle login")
    authenticatedUser = authenticate(email=email, password=password)

    try:
        if not authenticatedUser:
            print("in if section")
            user = MyUserModel.objects.filter(username=email)
            raise Exception("Failed to authenticate, maybe wrong username or password")
        print("logging user")
        print(authenticatedUser)
        login(req, authenticatedUser)
        log.info(f"Login success: {email}")
        return redirect("flight:feed")
    except Exception as e:
        log.info(f"Login failed for {email}: {str(e)}")
        return render(req, "authoriziation/login.html", {"status": "fail", "message": str(e)})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("user:login")

    def post(self, req):
        logout(req)
        log.info("Logout success")
        return redirect("login")


class ChargingAccount(LoginRequiredMixin, View):
    login_url = "user:login"

    def get(self, request):
        form_of_billing = bill()
        return render(request, "authoriziation/charging.html", {"form": form_of_billing})

    def post(self, request):
        credit_card = {
            "cc_number": request.POST.get("credit_card_number"),
            "credit_card_holder_name": request.POST.get("credit_card_holder_name"),
            "expiration_year": request.POST.get("expiration_year"),
            "expiration_month": request.POST.get("expiration_month"),
            'cvv': request.POST.get("cvv")
        }
        credit_card_value = bill(request.POST)
        person_pk = request.user.id
        if credit_card_value.is_valid() and person_pk:
            user = MyUserModel.objects.get(pk=person_pk)
            user.charge = user.charge + int(request.POST.get("bill"))
            user.save()
            log.info(f"user saved -> {user.id}")
            return redirect("flight:feed")
        else:
            form_errors = credit_card_value.errors
            return render(request, "authoriziation/charging.html",
                          {"forms": credit_card_value,
                           'form_errors': form_errors}, )
