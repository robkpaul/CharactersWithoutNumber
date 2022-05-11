from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout_view),
    path('login', auth_views.LoginView.as_view()),
    path('register', views.registration_view),
    path('home', views.home),
    path('campaign/<int:campaign_id>', views.campaign),
    path('character/<int:character_id>', views.character),
    path('create/character', views.create_character),
    path('create/campaign', views.create_campaign)
]