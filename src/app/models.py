from django.db import models
from django.contrib.auth.models import User

# Rule Models
class Background(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Vocation(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Focus(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Foci"

class Spell(models.Model):
    name = models.CharField(max_length=128)
    level = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.name, self.level)


class Item(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Armor(Item):
    ac = models.IntegerField()

    def __str__(self):
        return self.name

class Weapon(Item):
    atk = models.CharField(max_length=16)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.username

class Campaign(models.Model):
    title = models.CharField(max_length=127)
    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name="owned_campaigns"
    )
    players = models.ManyToManyField(Profile)

    def __str__(self):
        return self.title

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
    ac = models.IntegerField() # armor class
    strain = models.IntegerField(default=0) # system strain -- optional rule
    
    # Attributes
    atr_str = models.IntegerField(default=0) # strength
    atr_dex = models.IntegerField(default=0) # dexterity
    atr_con = models.IntegerField(default=0) # constitution
    atr_int = models.IntegerField(default=0) # intelligence
    atr_wis = models.IntegerField(default=0) # wisdom
    atr_cha = models.IntegerField(default=0) # charisma

    # Skills
    skl_admn = models.IntegerField(default=0) # administer
    skl_conn = models.IntegerField(default=0) # connect
    skl_conv = models.IntegerField(default=0) # convince
    skl_crft = models.IntegerField(default=0) # craft
    skl_exrt = models.IntegerField(default=0) # exert
    skl_heal = models.IntegerField(default=0) # heal
    skl_know = models.IntegerField(default=0) # know
    skl_lead = models.IntegerField(default=0) # lead
    skl_magc = models.IntegerField(default=0) # magic
    skl_noti = models.IntegerField(default=0) # notice
    skl_perf = models.IntegerField(default=0) # performance
    skl_pray = models.IntegerField(default=0) # pray
    skl_pnch = models.IntegerField(default=0) # punch
    skl_ride = models.IntegerField(default=0) # ride
    skl_sail = models.IntegerField(default=0) # sail
    skl_shot = models.IntegerField(default=0) # shot 
    skl_snek = models.IntegerField(default=0) # sneak
    skl_stab = models.IntegerField(default=0) # stab
    skl_srvv = models.IntegerField(default=0) # survive
    skl_trde = models.IntegerField(default=0) # trade
    skl_work = models.IntegerField(default=0) # work

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
        related_name='character_foci',
        blank=True,
        null = True
    )
    spells = models.ManyToManyField(
        Spell, 
        related_name='character_spells',
        blank=True,
        null = True
    )


    # Equipment and Inventory
    ## Currency
    wealth = models.PositiveIntegerField()  # measured in copper

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
        for i in self.inventory.all():
            item = {
                'type': 'item',
                'quantity': i.quantity,
                'equipped': i.equipped,
                'name': i.item.name
            }
            try:
                a = Armor.objects.get(pk=i.item.id)
                item['ac'] = a.ac
                item['type'] = 'armor'
            except Armor.DoesNotExist:
                try:
                    w = Weapon.objects.get(pk=i.item.id)
                    item['type'] = 'weapon'
                    item['atk'] = w.atk
                except Weapon.DoesNotExist:
                    pass
            print(item)
            sheet['inventory'].append(item)
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

    def __str__(self):
        return '%s (%s %s)' % (self.name, self.level, self.vocation)

class InventoryItem(models.Model):
    equipped = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="inventory")

    def __str__(self):
        return '%sx %s owned by %s' % (self.quantity, self.item, self.owner)