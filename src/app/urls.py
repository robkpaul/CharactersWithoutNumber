from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dicelog', views.dicelog),
    path('campaign/<int:campaign_id>', views.campaign),
    path('character/<int:character_id>', views.character)
]