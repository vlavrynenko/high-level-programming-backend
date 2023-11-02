from django.core import serializers
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .models import Character
from .models import Equipment
from .models import UserCharacters
from .models import Location
from .serializers import CharacterSerializer
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .location_controller import GetNearbyLocations, GetLocationNpc
from .inventory_utils import get_inventory, add_items, use_item, equip_item
import json

from .utils import serialize_one, deserialize_one, serialize_set, deserialize_set


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Attempt to create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Log the user in after registration
            login(request, user)

            # You can add more logic here like sending a confirmation email

            return redirect('profile')

        except IntegrityError as e:
            # Handle the exception for duplicate email or username
            messages.error(request, 'Username or email already exists.')

        except ValidationError as e:
            # Handle the exception for invalid email
            messages.error(request, 'Invalid email format.')

    return render(request, 'registration/register.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Redirect to the profile page
            return redirect('profile')
        else:
            # Display a login error message
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


@login_required
def profile(request):
    user = request.user


    user_characters = UserCharacters.objects.filter(user_id=request.user)
    char = serialize_set(user_characters)
    user_ch = deserialize_set(char)
    context = {
        'username': user.username,
        'user_characters': user_ch,
        # Add more user-specific data here if needed
    }

    request.session['context'] = {'user_characters': char}

    if request.method == 'POST':
        redirect('create_character')

    return render(request, 'registration/profile.html', context)


@api_view(['POST'])
@login_required
def create_character(request):
    user = request.user
    context = {'user': user}
    if request.method == 'POST':
        context = {'user': user}
        return render(request, 'registration/character_creation.html', context)

    return render(request, 'registration/character_creation.html', context)


@login_required
def save_character(request):
    user = request.user
    context = {'username': user.username}
    if request.method == 'POST':
        name = request.POST['character_name']
        race = request.POST['character_race']
        level = 1
        max_health = 50
        stats = {
            "current_health": 50,
            "stamina": 100,
            "current_stamina": 100,
            "mana": 0,
            "current_mana": 0,
            "health_regen": 1,
            "stamina_regen": 1,
            "mana_regen": 1,
            "strength": 10,
            "dexterity": 10,
            "intelligence": 0,
            "vitality": 10,
            "endurance": 10,
            "evasion_chance": 20,
            "damage_reduction": 0,
            "protection_head": 0,
            "protection_body": 0,
            "protection_legs": 0,
            "damage": 5
        }
        equipment = Equipment.objects.create(consumables={})
        inventory = {}
        current_location = Location.objects.get(id=1)
        character = Character.objects.create(name=name, race=race, max_health=max_health, level=level, stats=stats,
                                             equipment=equipment, inventory=inventory,
                                             current_location=current_location)
        current_character = UserCharacters.objects.create(user_id=user, character_id=character)
        return redirect('profile')
    return render(request, 'registration/character_creation.html', context)


@login_required
def initialize_game(request):
    context = {}
    session_context = request.session['context']
    if request.method == 'POST':
        character_id = request.POST['character_id']
        character = Character.objects.get(id=character_id)
        nearby_locations = GetNearbyLocations(character.current_location.id)
        location_npc, location_enemies = GetLocationNpc(character.current_location.id)
        inventory_json = json.loads(character.inventory)
        #inventory_json = get_inventory(character.inventory)
        #add_items([4, 7, 6], [1, 1, 1], inventory_json)
        #use_item(4, inventory_json)
        print(inventory_json)
        serialized_character = serialize_one(character)
        serialized_nearby_locations = serialize_set(nearby_locations)
        serialized_location_npc = serialize_set(location_npc)
        serialized_location_enemies = serialize_set(location_enemies)
        context = {'character': character,
                   'nearby_locations': nearby_locations,
                   'location_npc': location_npc,
                   'location_enemies': location_enemies,
                   'inventory': inventory_json}
        session_context['character'] = serialized_character
        session_context['nearby_locations'] = serialized_nearby_locations
        session_context['location_npc'] = serialized_location_npc
        session_context['location_enemies'] = serialized_location_enemies
        session_context['inventory'] = inventory_json
        request.session['context'] = session_context
        return render(request, 'registration/location.html', context)
    return render(request, 'registration/location.html')


@login_required
def load_location(request):
    user = request.user
    if request.method == 'POST':
        session_context = request.session.get('context')
        character = deserialize_one(session_context['character'])
        location_id = request.POST['location_id']
        new_location = Location.objects.get(id=location_id)
        character.current_location=new_location
        Character.objects.filter(id=character.id).update(current_location=new_location)
        nearby_locations = GetNearbyLocations(location_id)
        location_npc, location_enemies = GetLocationNpc(location_id)
        inventory = session_context['inventory']
        serialized_character = serialize_one(character)
        serialized_nearby_locations = serialize_set(nearby_locations)
        serialized_location_npc = serialize_set(location_npc)
        serialized_location_enemies = serialize_set(location_enemies)
        context = {'character': character,
                   'nearby_locations': nearby_locations,
                   'location_npc': location_npc,
                   'location_enemies': location_enemies,
                   'inventory': inventory}
        session_context['character'] = serialized_character
        session_context['nearby_locations'] = serialized_nearby_locations
        session_context['location_npc'] = serialized_location_npc
        session_context['location_enemies'] = serialized_location_enemies
        request.session['context'] = session_context
        return render(request, 'registration/location.html', context)


@login_required
def equip(request):
    if request.method == 'POST':
        print("Equip")
        session_context = request.session.get('context')
        item_to_equip = request.POST['item_id']
        print(f"Item id:{item_to_equip}")
        character = deserialize_one(session_context['character'])
        inventory = session_context['inventory']
        inventory = equip_item(item_to_equip, 1, character, inventory)
        nearby_locations = deserialize_set(session_context['nearby_locations'])
        location_npc = deserialize_set(session_context['location_npc'])
        location_enemies = deserialize_set(session_context['location_enemies'])
        context = {'character': character,
                   'nearby_locations': nearby_locations,
                   'location_npc': location_npc,
                   'location_enemies': location_enemies,
                   'inventory': inventory}
        session_context['inventory'] = inventory
        return render(request, 'registration/location.html', context)
        
        