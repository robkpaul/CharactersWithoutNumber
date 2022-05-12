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
                'username': request.user.username,
                'isowner': request.user.profile == campaign.owner
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

@login_required()
def create_character(request):
    if(request.method == 'POST'):
        form = forms.CharacterCreationForm(request.POST, user=request.user.profile)
        if(form.is_valid()):
            char = form.save()
            return redirect('/character/%s' % char.id)
        return redirect('/home')
    else:
        form = forms.CharacterCreationForm(user=request.user.profile)
    
    context = {
        'title': 'Create Character',
        'form': form,
        'text': 'In order to best create your character, I recommend utilizing the rules found in the first chapter of the <a href="https://www.drivethrurpg.com/product/348809/Worlds-Without-Number-Free-Edition">free version of Worlds Without Number.</a>',
        'button': 'Create'
    }
    return render(request, 'base_form.html', context=context)

@login_required()
def create_campaign(request):
    if(request.method == 'POST'):
        form = forms.CampaignCreationForm(request.POST, user=request.user.profile)
        if(form.is_valid()):
            campaign = form.save()
            return redirect('/campaign/%s' % campaign.id)
        return redirect('/home')
    else:
        form = forms.CampaignCreationForm(user=request.user.profile)
    
    context = {
        'title': 'Create Campaign',
        'form': form,
        'button': 'Create'
    }
    return render(request, 'base_form.html', context=context)

@login_required()
def add_char_to_campaign(request, **kwargs):
    cid = kwargs['character_id']
    char = Character.objects.get(pk=cid)
    if(request.user.profile == char.owner):
        if(request.method == 'POST'):
            form = forms.AddCharToCampaignForm(request.POST, user = request.user.profile, cid = cid)
            if(form.is_valid()):
                char = form.save()
                return redirect('/character/%s' % char.id)
            return redirect('/home')
        else:
            form = forms.AddCharToCampaignForm(user = request.user.profile, cid = cid)
        context = {
            'title': 'Add Character to Campaign',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access')

@login_required()
def add_player_to_campaign(request, **kwargs):
    cid = kwargs['campaign_id']
    camp = Campaign.objects.get(pk=cid)
    if(request.user.profile == camp.owner):
        if(request.method == 'POST'):
            form = forms.AddPlayerToCampaignForm(request.POST, cid = cid)
            if(form.is_valid()):
                camp= form.save()
                return redirect('/campaign/%s' % camp.id)
            return redirect('/home')
        else:
            form = forms.AddPlayerToCampaignForm(cid = cid)
        context = {
            'title': 'Add Player to Campaign',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access') 

@login_required()
def remove_player_from_campaign(request, **kwargs):
    cid = kwargs['campaign_id']
    camp = Campaign.objects.get(pk=cid)
    if(request.user.profile == camp.owner):
        if(request.method == 'POST'):
            form = forms.RemovePlayerFromCampaignForm(request.POST, cid = cid)
            if(form.is_valid()):
                camp= form.save()
                return redirect('/campaign/%s' % camp.id)
            return redirect('/home')
        else:
            form = forms.RemovePlayerFromCampaignForm(cid = cid)
        context = {
            'title': 'Remove Player',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access') 

@login_required()
def add_item_to_character(request, **kwargs):
    cid = kwargs['character_id']
    char = Character.objects.get(pk=cid)
    if(request.user.profile == char.owner):
        if(request.method == 'POST'):
            form = forms.AddItemToCharacterForm(request.POST, cid = cid)
            if(form.is_valid()):
                char = form.save()
                return redirect('/character/%s' % char.id)
            return redirect('/home')
        else:
            form = forms.AddItemToCharacterForm(cid = cid)
        context = {
            'title': 'Add Item',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access')

@login_required()
def add_foci_to_character(request, **kwargs):
    cid = kwargs['character_id']
    char = Character.objects.get(pk=cid)
    if(request.user.profile == char.owner):
        if(request.method == 'POST'):
            form = forms.AddFociToCharacterForm(request.POST, cid = cid)
            if(form.is_valid()):
                char = form.save()
                return redirect('/character/%s' % char.id)
            return redirect('/home')
        else:
            form = forms.AddFociToCharacterForm(cid = cid)
        context = {
            'title': 'Add Foci',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access')

@login_required()
def add_spell_to_character(request, **kwargs):
    cid = kwargs['character_id']
    char = Character.objects.get(pk=cid)
    if(request.user.profile == char.owner):
        if(request.method == 'POST'):
            form = forms.AddSpellToCharacterForm(request.POST, cid = cid)
            if(form.is_valid()):
                char = form.save()
                return redirect('/character/%s' % char.id)
            return redirect('/home')
        else:
            form = forms.AddSpellToCharacterForm(cid = cid)
        context = {
            'title': 'Add Spell',
            'form': form
        }
        return render(request, 'base_form.html', context=context)
    return HttpResponse('403: No Access')