from turtle import title
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user

from app.models import Background, Campaign, Character, Focus, InventoryItem, Item, Profile, Spell, Vocation

class RegistrationForm(UserCreationForm):
    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if(commit):
            user.save()
            profile = Profile.objects.create(user=user, username=user.username)
            profile.save()
        return user

class CharacterCreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('user')
        super(CharacterCreationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label='Name',
        max_length=64
    )
    hp = forms.IntegerField(label='Hit Points')
    atr_str = forms.IntegerField(label='Str') # strength
    atr_dex = forms.IntegerField(label='Dex') # dexterity
    atr_con = forms.IntegerField(label='Con') # constitution
    atr_int = forms.IntegerField(label='Int') # intelligence
    atr_wis = forms.IntegerField(label='Wis') # wisdom
    atr_cha = forms.IntegerField(label='Cha') # charisma

    skl_admn = forms.IntegerField(label='Administer') # administer
    skl_conn = forms.IntegerField(label='Connect') # connect
    skl_conv = forms.IntegerField(label='Convince') # convince
    skl_crft = forms.IntegerField(label='Craft') # craft
    skl_exrt = forms.IntegerField(label='Exert') # exert
    skl_heal = forms.IntegerField(label='Heal') # heal
    skl_know = forms.IntegerField(label='Know') # know
    skl_lead = forms.IntegerField(label='Lead') # lead
    skl_magc = forms.IntegerField(label='Magic') # magic
    skl_noti = forms.IntegerField(label='Notice') # notice
    skl_perf = forms.IntegerField(label='Performance') # performance
    skl_pray = forms.IntegerField(label='Pray') # pray
    skl_pnch = forms.IntegerField(label='Punch') # punch
    skl_ride = forms.IntegerField(label='Ride') # ride
    skl_sail = forms.IntegerField(label='Sail') # sail
    skl_shot = forms.IntegerField(label='Shoot') # shot 
    skl_snek = forms.IntegerField(label='Sneak') # sneak
    skl_stab = forms.IntegerField(label='Stab') # stab
    skl_srvv = forms.IntegerField(label='Survive') # survive
    skl_trde = forms.IntegerField(label='Trade') # trade
    skl_work = forms.IntegerField(label='Work') # work

    background = forms.ModelChoiceField(required=True, queryset=Background.objects.all())
    vocation = forms.ModelChoiceField(required=True, queryset=Vocation.objects.all())

    def save(self, commit=True):
        if commit:
            char = Character.objects.create(
                name = self.data['name'],
                hp = self.data['hp'],
                hp_max = self.data['hp'],
                atr_str = self.data['atr_str'],
                atr_dex = self.data['atr_dex'],
                atr_con = self.data['atr_con'],
                atr_int = self.data['atr_int'],
                atr_wis = self.data['atr_wis'],
                atr_cha = self.data['atr_cha'],
                skl_admn = self.data['skl_admn'],
                skl_conn = self.data['skl_conn'],
                skl_conv = self.data['skl_conv'],
                skl_crft = self.data['skl_crft'],
                skl_exrt = self.data['skl_exrt'],
                skl_heal = self.data['skl_heal'],
                skl_know = self.data['skl_know'],
                skl_lead = self.data['skl_lead'],
                skl_magc = self.data['skl_magc'],
                skl_noti = self.data['skl_noti'],
                skl_perf = self.data['skl_perf'],
                skl_pray =self.data['skl_pray'],
                skl_pnch = self.data['skl_pnch'],
                skl_ride = self.data['skl_ride'],
                skl_sail = self.data['skl_sail'],
                skl_shot = self.data['skl_shot'],
                skl_snek = self.data['skl_snek'],
                skl_stab = self.data['skl_stab'],
                skl_srvv = self.data['skl_srvv'],
                skl_trde = self.data['skl_trde'],
                skl_work = self.data['skl_work'],
                background = Background.objects.get(pk=self.data['background']),
                vocation = Vocation.objects.get(pk=self.data['vocation']),
                owner = self.owner
            )
            char.save()
            return char
        return None

class CampaignCreationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('user')
        super(CampaignCreationForm, self).__init__(*args, **kwargs)
    title = forms.CharField(max_length=64)

    def save(self, commit=True):
        if commit:
            campaign = Campaign.objects.create(
                title = self.data['title'],
                owner = self.owner
            )
            return campaign
        return None

class AddCharToCampaignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('user')
        self.char = Character.objects.get(pk=kwargs.pop('cid'))
        super(AddCharToCampaignForm, self).__init__(*args, **kwargs)
        self.fields['campaign'].queryset = self.owner.participant_campaigns
    
    campaign = forms.ModelChoiceField(
        required=True,
        queryset= Campaign.objects.all()
    )
    
    def save(self, commit=True):
        if commit:
            self.char.campaign = Campaign.objects.get(pk=self.data['campaign'])
            self.char.save()
            return self.char
        return None

class AddPlayerToCampaignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.campaign = Campaign.objects.get(pk=kwargs.pop('cid'))
        super(AddPlayerToCampaignForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(
        max_length=64,
        label='Username'
    )

    def clean(self):
        try:
            player = Profile.objects.get(username=self.data['username'])
        except Profile.DoesNotExist:
            raise forms.ValidationError(u"User does not exist.")
    def save(self, commit=True):
        if commit:
            player = Profile.objects.get(username=self.data['username'])
            if player != self.campaign.owner:
                self.campaign.players.add(player)
                self.campaign.save()
            return self.campaign
        return None

class RemovePlayerFromCampaignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.campaign = Campaign.objects.get(pk=kwargs.pop('cid'))
        super(RemovePlayerFromCampaignForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = self.campaign.players
    
    player= forms.ModelChoiceField(
        required=True,
        queryset= Profile.objects.all()
    )
    
    def save(self, commit=True):
        if commit:
            player = Profile.objects.get(pk=self.data['player'])
            self.campaign.players.remove(player)
            # TODO: Remove characters from the player being removed
            self.campaign.save()
            return self.campaign
        return None

class AddItemToCharacterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.char = Character.objects.get(pk=kwargs.pop('cid'))
        super(AddItemToCharacterForm, self).__init__(*args, **kwargs)
    
    item = forms.ModelChoiceField(
        required=True,
        queryset= Item.objects.all()
    )
    quantity = forms.IntegerField(
        min_value=1, 
        required=True
    )
    
    def save(self, commit=True):
        if commit:
            InventoryItem.objects.create(
                owner=self.char,
                item = Item.objects.get(pk=self.data['item']),
                quantity = self.data['quantity']
            )
            self.char.save()
            return self.char
        return None

class AddSpellToCharacterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.char = Character.objects.get(pk=kwargs.pop('cid'))
        super(AddSpellToCharacterForm, self).__init__(*args, **kwargs)
    
    spell = forms.ModelChoiceField(
        required=True,
        queryset= Spell.objects.all()
    )
    def save(self, commit=True):
        if commit:
            self.char.spells.add(Spell.objects.get(pk=self.data['spell']))
            self.char.save()
            return self.char
        return None

class AddFociToCharacterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.char = Character.objects.get(pk=kwargs.pop('cid'))
        super(AddFociToCharacterForm, self).__init__(*args, **kwargs)
        #self.fields['foci'].queryset = Focus.objects.filter(character_foci__id__contains=self.char.id)
    
    foci = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Focus.objects.all()
    )
    def save(self, commit=True):
        if commit:
            for f in self.data['foci']:
                self.char.foci.add(Focus.objects.get(pk=f))
            self.char.save()
            return self.char
        return None