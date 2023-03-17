# prototype/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('auth_app.urls')),  # Change 'auth/' to ''
]
