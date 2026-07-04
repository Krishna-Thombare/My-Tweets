from django.contrib import admin
from .models import Tweet, Profile, CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(CustomUser, UserAdmin)