from enum import unique
from django.db import models
from django.contrib.auth.models import User as auth_user

class Profile(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.ForeignKey(
        auth_user,
        on_delete=models.Cascade
    )
    