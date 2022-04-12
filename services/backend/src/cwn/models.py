from django.db import models
from django.contrib.auth.models import User

class Character():
    name = models.CharField(max_length=127)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Campaign():
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)