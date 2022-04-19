from django.db import models
from django.contrib.auth.models import User


# Custom Dice Field
class DiceField(models.Field):
    description = "A d3, d4, d6, d8, d10, d12, d20, or d100"

# Rule Models

class Background(models.Model):
    name = models.CharField()

class Vocation(models.Model):
    name = models.CharField()

class Focus(models.Model):
    name = models.CharField()

class Spell(models.Model):
    name = models.CharField()
    level = models.IntegerField()

class Item(models.Model):
    name = models.CharField()

class Equipable(Item):
    equipped = models.BooleanField()

class Armor(Equipable):
    ac = models.IntegerField()

class Weapon(Equipable):
    atk = models.IntegerField()


# Models for the App
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32, null=False)

class Campaign(models.Model):
    title = models.CharField(max_length=127)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owned_campaigns")
    players = models.ManyToManyField(Profile)

#Character Sheet Models

class Character(models.Model):
    # Character Sheet Data
    name = models.CharField(max_length=64, default='steve')
    level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0) # xp -- optional rule
    hp = models.IntegerField() # current hit points
    hp_max = models.IntegerField() # maximum hit points
    ac = models.IntegerField # armor class
    strain = models.IntegerField(default=0) # system strain -- optional rule
    
    # Attributes
    atr_str = models.IntegerField() # strength
    atr_dex = models.IntegerField() # dexterity
    atr_con = models.IntegerField() # constitution
    atr_int = models.IntegerField() # intelligence
    atr_wis = models.IntegerField() # wisdom
    atr_cha = models.IntegerField() # charisma

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

    # Character Attributes that are handled by other Models
    background = models.ForeignKey(Background, related_name='character_backgrounds')
    vocation = models.ForeignKey(Vocation, related_name='character_vocations')
    foci = models.ManyToManyField(Focus, related_name='character_foci')
    spells = models.ManyToManyField(Spell, related_name='character_spells')


    # Equipment and Inventory
    ## Currency
    gold = models.IntegerField()
    silver = models.IntegerField()

    # Metadata - External to Character Sheet, used by the app itself
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, related_name="characters")

    @property
    def full(self):
        "Returns the full character sheet, with all info"
        return ''

    @property
    def brief(self):
        "Returns the partial character sheet, with only the info needed for the DM Screen"
        sheet = {}
        sheet['name'] = self.name
        sheet['hp'] = self.hp
        sheet['hp_max'] = self.hp_max
        sheet['ac'] = self.ac
        sheet['level'] = self.level
        sheet['class'] = self.vocation
        return sheet


class InventoryItem(models.Model):
    """Handles the inventory of a character"""
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField()