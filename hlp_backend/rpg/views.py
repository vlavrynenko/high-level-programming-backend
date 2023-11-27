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
from .forms import CharacterListForm  # Import the CharacterListForm


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

    context = {
        'username': user.username,
        'user_characters': user_characters,
        # Add more user-specific data here if needed
    }

    return render(request, 'registration/profile.html', context)


@api_view(['POST'])
def create_character(request):
    user = request.user
    context = {'user': user}
    if request.method == 'POST':
        redirect('create_character')

    return render(request, 'registration/character_creation.html', context)


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
        character = Character.objects.create(name=name, race=race, max_health=max_health, level=level, stats=stats, equipment=equipment, inventory=inventory, current_location=current_location)
        current_character = UserCharacters.objects.create(user_id=user, character_id=character)
        return redirect('profile')
    return render(request, 'registration/character_creation.html', context)


