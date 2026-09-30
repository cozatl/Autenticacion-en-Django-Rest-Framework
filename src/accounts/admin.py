from django.contrib import admin

from .models import GuestEmail, User

admin.site.register(User)
admin.site.register(GuestEmail)
