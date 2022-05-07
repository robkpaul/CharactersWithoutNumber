from django.shortcuts import render
from django.http import HttpResponse
from app.models import Campaign, Character

def index(request):
    return render(request, 'index.html')

def campaign(request, **kwargs):
    cid = kwargs['campaign_id']
    try:
        campaign = Campaign.objects.get(pk=cid)
        context = {
            'campaign_id': cid,
            'chars': [], # handled in for loop
            'campaign': campaign.title,
            'username': 'rokepa'
        }
        for c in campaign.characters.all():
            context['chars'].append(c.brief())

        return render(request, 'campaign.html', context=context )
    except Campaign.DoesNotExist:
        return HttpResponse('404: Campaign Does Not Exist')

def character(request, **kwargs):
    cid = kwargs['character_id']
    character = Character.objects.get(pk=cid)
    context = {
        'sheet': character.full()
    }
    return render(request, 'character.html', context=context)