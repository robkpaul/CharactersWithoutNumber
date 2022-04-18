from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def index(request):
    context = {
        'title': 'Home'
    }
    