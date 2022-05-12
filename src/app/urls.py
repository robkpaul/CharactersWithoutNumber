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
    path('create/campaign', views.create_campaign),
    path('character/<int:character_id>/add_campaign', views.add_char_to_campaign),
    path('campaign/<int:campaign_id>/add_player', views.add_player_to_campaign),
    path('campaign/<int:campaign_id>/remove_player', views.remove_player_from_campaign),
    path('character/<int:character_id>/add_item', views.add_item_to_character),
    path('character/<int:character_id>/add_spell', views.add_spell_to_character),
    path('character/<int:character_id>/add_foci', views.add_foci_to_character)
]