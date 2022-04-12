from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    name = models.CharField(max_length=127)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="characters")

class Campaign(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_campaigns")
    players = models.ManyToManyField(User)