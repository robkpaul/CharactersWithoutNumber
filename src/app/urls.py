from django.urls import path
from . import views

urlpatterns = [
    path('', views.getTest),
    path('character/', views.getCharacter)
]