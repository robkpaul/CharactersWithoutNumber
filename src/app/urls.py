from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dicelog', views.dicelog)
    #,path('character/', views.character)
]