from django.db import models
from django.contrib.auth.models import User

# Rule Models
class Background(models.Model):
    name = models.CharField(max_length=128)

class Vocation(models.Model):
    name = models.CharField(max_length=128)

class Focus(models.Model):
    name = models.CharField(max_length=128)

class Spell(models.Model):
    name = models.CharField(max_length=128)
    level = models.IntegerField()

class Item(models.Model):
    name = models.CharField(max_length=128)

class Equipable(Item):
    equipped = models.BooleanField()

    class Meta:
        abstract = True

class Armor(Equipable):
    ac = models.IntegerField()

class Weapon(Equipable):
    atk = models.PositiveIntegerField()


# Models for the App
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    username = models.CharField(
        max_length=32, 
        null=False
    )

class Campaign(models.Model):
    title = models.CharField(max_length=127)
    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name="owned_campaigns"
    )
    players = models.ManyToManyField(Profile)

#Character Sheet Models

class Character(models.Model):
    # Character Sheet Data
    name = models.CharField(
        max_length=64, 
        default='Thorin Thabiticus'
    )
    level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0) # xp -- optional rule
    hp = models.PositiveIntegerField() # current hit points
    hp_max = models.PositiveIntegerField() # maximum hit points
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
    background = models.ForeignKey(
        Background, 
        related_name='character_backgrounds', 
        null=True, 
        on_delete=models.SET_NULL
    )
    vocation = models.ForeignKey(
        Vocation, 
        related_name='character_vocations', 
        null=True, 
        on_delete=models.SET_NULL
    )
    foci = models.ManyToManyField(
        Focus, 
        related_name='character_foci'
    )
    spells = models.ManyToManyField(
        Spell, 
        related_name='character_spells'
    )


    # Equipment and Inventory
    ## Currency
    wealth = models.PositiveIntegerField()  # measured in copper

    ## Inventory
    items = models.ManyToManyField(
        Item,
        related_name='character_items'
    )
    armor = models.ManyToManyField(
        Armor,
        related_name='character_armor'
    )
    weapons = models.ManyToManyField(
        Weapon,
        related_name='character_weapons'
    )

    # Metadata - External to Character Sheet, used by the app itself
    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        Campaign, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='characters'
    )

    # Methods
    def full(self):
        """Returns the full character sheet, with all info"""
        sheet = {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'hp_max': self.hp_max,
            'ac': self.ac,
            'strain': self.strain,
            'attributes': {
                'str': self.atr_str,
                'dex': self.atr_dex,
                'con': self.atr_con,
                'int': self.atr_int,
                'wis': self.atr_wis,
                'cha': self.atr_cha
            },
            'skills': {
                'administer': self.skl_admn,
                'connect': self.skl_conn,
                'convince': self.skl_conv,
                'craft': self.skl_crft,
                'exert': self.skl_exrt,
                'heal': self.skl_heal,
                'know': self.skl_know,
                'lead': self.skl_know,
                'magic': self.skl_magc,
                'notice': self.skl_noti,
                'perform': self.skl_perf,
                'pray': self.skl_pray,
                'punch': self.skl_pnch,
                'ride': self.skl_ride,
                'sail': self.skl_sail,
                'shoot': self.skl_shot,
                'sneak': self.skl_snek,
                'stab': self.skl_stab,
                'survive': self.skl_srvv,
                'trade': self.skl_trde,
                'work': self.skl_work
            },
            'background': self.background.name,
            'vocation': self.vocation.name,
            'foci': [],
            'spells': [],
            'wealth':  self.wealth,
            'inventory': [],
        }
        # Many to Many fields are handled through loops
        for f in self.foci.all():
            sheet['foci'].append(f.name)

        for s in self.spells.all():
            sheet['spells'].append({
                'name': s.name,
                'level': s.level
            })
        for i in self.items.all():
            sheet['inventory'].append({
                'type': 0,
                'name': i.name
            })
        for i in self.armor.all():
            sheet['inventory'].append({
                'type': 'armor',
                'name': i.name,
                'equipped': i.equipped,
                'ac': i.ac
            })
        for i in self.weapons.all():
            sheet['inventory'].append({
                'type': 'armor',
                'name': i.name,
                'equipped': i.equipped,
                'attack': i.atk
            })

        return sheet

    def brief(self):
        """Returns the partial character sheet, with only the info needed for the DM Screen"""
        sheet = {}
        sheet['name'] = self.name
        sheet['hp'] = self.hp
        sheet['hp_max'] = self.hp_max
        sheet['ac'] = self.ac
        sheet['notice'] = self.skl_noti
        sheet['level'] = self.level
        sheet['class'] = self.vocation
        return sheet


class InventoryItem(models.Model):
    """Handles the inventory of a character"""
    owner = models.ForeignKey(Character, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField()