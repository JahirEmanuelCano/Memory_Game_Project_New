from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
        # AJAX endpoint to flip a card
    path('flip/<int:index>/', views.flip_card, name='flip'),
    # Reset the current game
    path('restart/', views.restart_game, name='restart'),
    # Transition to memorizing phase
    path('start-memorizing/', views.start_memorizing, name='start_memorizing'),
    # Transition to playing phase
    path('start-playing/', views.start_playing, name='start_playing'),
]
