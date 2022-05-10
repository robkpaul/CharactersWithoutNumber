from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from app.models import Campaign, Character, Profile
from . import forms

@login_required()
def index(request):
    return redirect('/home')

def logout_view(request):
    logout(request)
    return redirect('/login')

def registration_view(request):
    if(request.method == 'POST'):
        form = forms.RegistrationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/login')
    else:
        form = forms.RegistrationForm()
    
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'registration/register.html', context=context)

@login_required()
def home(request):
    profile = request.user.profile
    context = {
        'chars': [],
        'campaigns': [],
        'username': profile.username
    }   
    for c in profile.characters.all():
        context['chars'].append({
            'text': str(c),
            'id': c.id
        })
    for c in profile.participant_campaigns.all():
        context['campaigns'].append({
            'text': str(c),
            'id': c.id,
            'owner': False
        })
    for c in profile.owned_campaigns.all():
        context['campaigns'].append({
            'text': str(c),
            'id': c.id,
            'owner': True
        })
    print(context)
    return render(request, 'home.html', context=context)

@login_required()
def campaign(request, **kwargs):
    cid = kwargs['campaign_id']
    try:
        campaign = Campaign.objects.get(pk=cid)
        print(campaign.players.all())
        if(campaign.owner == request.user.profile or request.user.profile in campaign.players.all()):
            context = {
                'campaign_id': cid,
                'chars': [], # handled in for loop
                'campaign': campaign.title,
                'username': request.user.username  
            }
            for c in campaign.characters.all():
                context['chars'].append(c.brief())

            return render(request, 'campaign.html', context=context )
    except Campaign.DoesNotExist:
        pass
    return HttpResponse('403: No Access')

@login_required()
def character(request, **kwargs):
    cid = kwargs['character_id']
    try:
        character = Character.objects.get(pk=cid)
        if(character.owner == request.user.profile):
            context = {
                'sheet': character.full(),
                'username': request.user.username,
                'campaign_id': -1
            }
            if(character.campaign):
                context['campaign_id'] = character.campaign.id
            return render(request, 'character.html', context=context)
    except Character.DoesNotExist:
        pass
    return HttpResponse('403: No Access')