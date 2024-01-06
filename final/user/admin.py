from django.contrib import admin
from .models import MyUserModel, Profile
admin.site.register(MyUserModel)
admin.site.register(Profile)