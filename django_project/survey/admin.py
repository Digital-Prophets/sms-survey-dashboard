from django.contrib import admin
from .models import Client

admin.site.register(Client)
admin.site.site_header  =  "SMS Survey Dashboard"
