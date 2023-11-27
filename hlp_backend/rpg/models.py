from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    trigger = models.CharField('location trigger')
    neighbour_locations = models.JSONField()

    def __str__(self):
        return self.id


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    trigger = models.CharField('action trigger')
    description = models.CharField('action description')
    command = models.JSONField()

    def __str__(self):
        return self.id


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    trigger = models.CharField('item trigger')
    stats = models.JSONField()
    drop_chance = models.IntegerField()

    def __str__(self):
        return self.id


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('skill name')
    description = models.CharField('skill description')
    trigger = models.CharField('skill trigger')
    active = models.BooleanField()
    stats = models.JSONField()

    def __str__(self):
        return self.id


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    helmet = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_helmets', default=0)
    breastplate = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_breastplates',
                                    default=0)
    leggings = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_leggings',
                                 default=0)
    shoulders = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_shoulders',
                                  default=0)
    bracers = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_bracers',
                                default=0)
    chainmail = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_chainmails',
                                  default=0)
    boots = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_boots', default=0)
    weapon_right = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_right_weapons',
                                     default=0)
    weapon_left = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_left_weapons',
                                    default=0)
    ring = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_rings', default=0)
    amulet = models.ForeignKey(Item, on_delete=models.SET(0), related_name='%(class)s_amulets', default=0)
    consumables = models.JSONField(default='{}')

    def __str__(self):
        return self.id


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name')
    race = models.CharField('race')
    max_health = models.IntegerField()
    level = models.IntegerField()
    stats = models.JSONField()
    equipment = models.ForeignKey(Equipment, on_delete=models.SET(0))
    inventory = models.JSONField()
    current_location = models.ForeignKey(Location, on_delete=models.SET(0))
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id


class Npc(models.Model):
    id = models.AutoField(primary_key=True)
    character_id = models.OneToOneField(Character, on_delete=models.SET(0))
    trigger = models.CharField('npc trigger')
    drop_multiplier = models.FloatField()
    drop_list = models.JSONField()

    def __str__(self):
        return self.id


class Quest(models.Model):
    id = models.AutoField(primary_key=True)
    npc_id = models.ForeignKey(Npc, on_delete=models.SET(0))
    name = models.CharField('skill name')
    description = models.CharField('Quest description')
    trigger = models.CharField('quest trigger')
    min_level = models.IntegerField()

    def __str__(self):
        return self.id


class QuestStep(models.Model):
    id = models.AutoField(primary_key=True)
    step_order = models.IntegerField()
    quest_id = models.ForeignKey(Quest, on_delete=models.SET(0))
    description = models.CharField('quest step description')
    trigger = models.CharField('quest step trigger')

    def __str__(self):
        return self.id


class UserQuest(models.Model):
    id = models.AutoField(primary_key=True)
    quest_id = models.ForeignKey(Quest, on_delete=models.SET(0))
    current_step = models.ForeignKey(QuestStep, on_delete=models.SET(0))
    done = models.BooleanField(default=False)
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id


class CharacterSkills(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)


class UserCharacters(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class FightSession(models.Model):
    id = models.AutoField(primary_key=True)
    first_side = models.JSONField()
    second_side = models.JSONField()
    winner_side = models.BooleanField()
    location = models.ForeignKey(Location, on_delete=models.SET(0))
    created_at = models.DateField(auto_now_add=True)
    ended_at = models.DateField()

    def __str__(self):
        return self.id


class FightAction(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(FightSession, on_delete=models.CASCADE)
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='%(class)s_characters')
    target_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    action = models.JSONField()

    def __str__(self):
        return self.id


class UserFightSession(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.ForeignKey(FightSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class TempCharacter(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.BooleanField()
    alive = models.BooleanField()
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    session_id = models.ForeignKey(FightSession, on_delete=models.CASCADE)
    name = models.CharField('name')
    race = models.CharField('race')
    max_health = models.IntegerField()
    level = models.IntegerField()
    stats = models.JSONField()
    equipment = models.ForeignKey(Equipment, on_delete=models.SET(0))

    def __str__(self):
        return self.id


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    open = models.BooleanField()
    seller = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='%(class)s_sellers')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Character, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    ended_at = models.DateField()

    def __str__(self):
        return self.id


class ItemAction(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    action_id = models.ForeignKey(Action, on_delete=models.CASCADE)


class NpcAction(models.Model):
    npc_id = models.ForeignKey(Npc, on_delete=models.CASCADE)
    action_id = models.ForeignKey(Action, on_delete=models.CASCADE)
