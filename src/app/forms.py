from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user
from django.core.validators import validate_slug, validate_email

from app.models import Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if(commit):
            user.save()
            profile = Profile.objects.create(user=user, username=user.username)
            profile.save()
        return user