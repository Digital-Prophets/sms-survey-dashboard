# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
app_name = "survey"
urlpatterns = [
   path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)