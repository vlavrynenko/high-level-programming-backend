from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from .models import User


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User(username=username, email=email, password=password)
        user.save()
        # You can add more logic here like sending a confirmation email
        return redirect('profile')
    return render(request, 'registration/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, password=password)
            # Perform login logic here, e.g., set session variables
            return render(request, 'registration/profile.html', {'username': user.username})
        except ObjectDoesNotExist:
            # Handle login error
            return render(request, 'registration/login.html', {'show_notification': True})
            pass
    return render(request, 'registration/login.html')


def profile(request):
    # Add code to display the user's profile
    return render(request, 'registration/profile.html')