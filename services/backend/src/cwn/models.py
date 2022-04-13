from django.db import models
from django.contrib.auth.models import User


def sheet_default():
    sheet = { # Fields that all sheets have, detailed breakdown of the character sheet can be found on Page 6-8 of the Worlds Without Number rulebook.
        'name': '',
        'level': 0,
        'xp': 0,
        'max_hp': '',
        'curr_hp': '',
        'strain': 0,
        'ac': 0,
        'stats': {
                'str': 0,
                'dex': 0,
                'con': 0,
                'int': 0,
                'wis': 0,
                'cha': 0
        },
        'saves': {
            'physical': 0,
            'evasion': 0,
            'mental': 0,
            'luck': 0,
        },
        'background': '',
        'class': [], # list because can be just 1 field, or two fields for a Mage (Mage + Subclass), or up to 5 in the case of an Adventurer who chooses to double Mage
        'skills': {},
        'foci': [],
        'spells': [],
        'armor': [],
        'weapons': [],
        'inventory': [],
    }
    return sheet

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32, null=False)

class Character(models.Model):
    # Character Sheet Data
    name = models.CharField(max_length=64, default='steve')
    level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    max_hp = models.IntegerField()
    curr_hp = models.IntegerField()
    strain = models.IntegerField(default=0)
    
    # Metadata - External to Character Sheet
    sheet = models.JSONField(default=sheet_default())
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="characters")

    def getStat(self, stat):
        return self.sheet['stats'][stat]


class Campaign(models.Model):
    title = models.CharField(max_length=127)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owned_campaigns")
    players = models.ManyToManyField(Profile)