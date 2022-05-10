from django.shortcuts import redirect, render
from django.http import HttpResponse
from app.models import Campaign, Character, Profile

def index(request):
    return redirect('home')

def home(request):
    context = {}
    profile = Profile.objects.get(pk=1)
    #profile = request.user.profile
    context['username'] = profile.username
    return render(request, 'home.html', context=context)

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
    try:
        character = Character.objects.get(pk=cid)
        context = {
            'sheet': character.full(),
            'username': 'rokepa',
            'campaign_id': character.campaign.id
        }
        return render(request, 'character.html', context=context)
    except Character.DoesNotExist:
        return HttpResponse('404: Character Does Not Exist')