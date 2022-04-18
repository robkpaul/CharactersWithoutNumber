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

class Campaign(models.Model):
    title = models.CharField(max_length=127)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owned_campaigns")
    players = models.ManyToManyField(Profile)

class Character(models.Model):
    # Character Sheet Data
    name = models.CharField(max_length=64, default='steve')
    level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    hp = models.IntegerField()
    hp_max = models.IntegerField()
    strain = models.IntegerField(default=0)
    
    # Attributes
    atr_str = models.IntegerField()
    atr_dex = models.IntegerField()
    atr_con = models.IntegerField()
    atr_int = models.IntegerField()
    atr_wis = models.IntegerField()
    atr_cha = models.IntegerField()

    # Skills
    skl_admn = models.IntegerField() # administer
    skl_conn = models.IntegerField() # connect
    skl_conv = models.IntegerField() # convince
    skl_crft = models.IntegerField() # craft
    skl_exrt = models.IntegerField() # exert
    skl_heal = models.IntegerField() # heal
    skl_know = models.IntegerField() # know
    skl_lead = models.IntegerField() # lead
    skl_magc = models.IntegerField() # magic
    skl_noti = models.IntegerField() # notice
    skl_perf = models.IntegerField() # performance
    skl_pray = models.IntegerField() # pray
    skl_pnch = models.IntegerField() # punch
    skl_ride = models.IntegerField() # ride
    skl_sail = models.IntegerField() # sail
    skl_shot = models.IntegerField() # shot 
    skl_snek = models.IntegerField() # sneak
    skl_stab = models.IntegerField() # stab
    skl_srvv = models.IntegerField() # survive
    skl_trde = models.IntegerField() # trade
    skl_work = models.IntegerField() # work

    # Other properties, handled by rules
    background = models.ForeignKey('rules.Background', related_name='character_backgrounds')
    vocation = models.ForeignKey('rules.Vocation', related_name='character_vocations')
    foci = models.ManyToManyField('rules.Focus', related_name='character_foci')

    # Equipment and Inventory
    ## Currency
    gold = models.IntegerField()
    silver = models.IntegerField()

    ## Equipment
    

    # Metadata - External to Character Sheet, used by the API itself
    sheet = models.JSONField(default=sheet_default())
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="characters")