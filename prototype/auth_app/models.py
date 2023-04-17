from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    facial_data = models.JSONField(null=True, blank=True)
    password = models.CharField(max_length=128)

    def check_password(self, raw_password):
        # Retrieve the hashed password from the `auth_app_customer` table
        # and use Django's `check_password` method to verify the password
        return check_password(raw_password, self.password)