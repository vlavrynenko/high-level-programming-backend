from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('character_creation/', views.create_character, name='create_character'),
    path('save_character/', views.save_character, name='save_character'),
    path('game/', views.initialize_game, name='initialize_game'),
    path('location/', views.load_location, name='load_location'),
    path('equip/', views.equip, name='equip')
]