from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app.models import Campaign, Character

def index(request):
    return render(request, 'index.html')

def dicelog(request):
    return render(request, 'dicelog.html')

def campaign(request, **kwargs):
    cid = kwargs['campaign_id']
    campaign = 1 #Campaign.objects.get(pk=cid)
    context = {
        'campaign_id': cid,
        'chars': [], # handled in for loop
        'campaign': 'test'#campaign.name
    }
    context['chars'].append({
                'name': 'Thorin Thabiticus',
                'hp_max': 10,
                'ac': 20,
                'level': 1,
                'class': 'Warrior',
                'notice': 10
    })
    # for c in campaign.characters.all():
    #     context['chars'].append(c.brief())

    return render(request, 'campaign.html', context=context )

def character(request, **kwargs):
    cid = kwargs['character_id']
    character = Character.objects.get(pk=cid)
    context = {
        'sheet': character.full()
    }
    return render(request, 'character.html', context=context)