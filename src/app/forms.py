from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user
from django.core.validators import validate_slug, validate_email

from app.models import Background, Character, Profile, Vocation

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
    name_field = forms.CharField(
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
                name = self.name,
                hp = self.hp,
                hp_max = self.hp,
                atr_str = self.atr_str,
                atr_dex = self.atr_dex,
                atr_con = self.atr_con,
                atr_int = self.atr_int,
                atr_wis = self.atr_wis,
                atr_cha = self.atr_cha,
                skl_admn = self.skl_admn,
                skl_conn = self.skl_conn,
                skl_conv = self.skl_conv,
                skl_crft = self.skl_crft,
                skl_exrt = self.skl_exrt,
                skl_heal = self.skl_heal,
                skl_know = self.skl_know,
                skl_lead = self.skl_lead,
                skl_magc = self.skl_magc,
                skl_noti = self.skl_noti,
                skl_perf = self.skl_perf,
                skl_pray =self.skl_pray,
                skl_pnch = self.skl_pnch,
                skl_ride = self.skl_ride,
                skl_sail = self.skl_sail,
                skl_shot = self.skl_shot,
                skl_snek = self.skl_snek,
                skl_stab = self.skl_stab,
                skl_srvv = self.skl_srvv,
                skl_trde = self.skl_trde,
                skl_work = self.skl_work,
                background = self.background,
                vocation = self.vocation,
                owner = self.owner
            )
            char.save()

            def __init__(self, user, *args, **kwargs):
                self.owner = user
                super(CharacterCreationForm, self).__init__(*args, **kwargs)

        return char