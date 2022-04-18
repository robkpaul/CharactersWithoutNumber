from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app.models import Character


def index(request):
    response = 'Online'
    return HttpResponse(response)

def character(request, id=0):
    response = {}
    sheet = Character.objects.get(pk=id)
    response['sheet'] = sheet.full()
    return JsonResponse(response)

def characterBrief(request, id=0):
    response = {}
    sheet = Character.objects.get(pk=id)
    response['sheet'] = sheet.brief()
    return JsonResponse(response)