from django.db import models
from django.contrib.auth.models import User

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
    spells = models.ManyToManyField('rules.Spell', related_name='character_spells')


    # Equipment and Inventory
    ## Currency
    gold = models.IntegerField()
    silver = models.IntegerField()

    ## Equipment
    inventory = models.ManyToManyField('rules.Items', related_name='character_items')
    armor = models.ManyToManyField('rules.Armor', related_name='character_armor')
    weapons = models.ManyToManyField('rules.Weapon', related_name='character_weapons')

    # Metadata - External to Character Sheet, used by the API itself
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="characters")