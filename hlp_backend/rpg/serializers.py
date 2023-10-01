from rest_framework import serializers

from .models import Action
from .models import Auction
from .models import Character
from .models import Equipment
from .models import FightAction
from .models import FightSession
from .models import Item
from .models import ItemAction
from .models import Npc
from .models import NpcAction
from .models import Quest
from .models import QuestStep
from .models import Skill
from .models import TempCharacter
from .models import User
from .models import UserFightSession
from .models import UserQuest


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'trigger', 'description', 'command']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'type', 'trigger', 'stats', 'drop_chance']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'trigger', 'active', 'stats']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'helmet', 'breastplate', 'leggings', 'shoulders', 'bracers', 'chainmail', 'boots',
                  'weapon_right', 'weapon_left', 'ring', 'amulet', 'consumables']


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'race', 'max_health', 'level', 'stats', 'equipment', 'inventory', 'current_location',
                  'created_at']


class NpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Npc
        fields = ['id', 'character_id', 'trigger', 'drop_multiplier', 'drop_list']


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'npc_id', 'name', 'description', 'trigger', 'min_level']


class QuestStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestStep
        fields = ['id', 'step_order', 'quest_id', 'description', 'trigger']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at']


class UserQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuest
        fields = ['id', 'quest_id', 'current_step', 'done', 'character_id', 'user_id', 'created_at']


class FightSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightSession
        fields = ['id', 'first_side', 'second_side', 'winner_side', 'location', 'created_at', 'ended_at']


class FightActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FightAction
        fields = ['id', 'session_id', 'character_id', 'target_id', 'action']


class UserFightSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFightSession
        fields = ['id', 'user_id', 'session_id']


class TempCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempCharacter
        fields = ['id', 'user', 'alive', 'character_id', 'session_id', 'name', 'race', 'max_health', 'level', 'stats',
                  'equipment']


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'open', 'seller', 'item', 'buyer', 'created_at', 'ended_at']


class ItemActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAction
        fields = ['item_id', 'action_id']


class NpcActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NpcAction
        fields = ['npc_id', 'action_id']
