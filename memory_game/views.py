"""Django views for the Memory Game application."""

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .logic import GameBoard
import random
# Key used to store the serialized :class:`GameBoard` in the session
SESSION_KEY = 'game_state'

def set_difficulty(request, level):
    """
    Set the game difficulty and initialize a new game.
    Difficulty can be: 'facil', 'medio', 'dificil'
    """
    levels = {
        'facil': 3,    # 3 pairs = 6 cards
        'medio': 6,    # 6 pairs = 12 cards
        'dificil': 12  # 12 pairs = 24 cards
    }
    num_pairs = levels.get(level, 3)  # Default to 'facil'

    # Store difficulty in session
    request.session['difficulty'] = level

    # Create a new GameBoard with the desired number of pairs
    game = GameBoard.new_game(num_pairs)
    request.session[SESSION_KEY] = game.to_dict()

    # Return JSON for frontend to update
    response = {
        'cards': game.cards,
        'states': game.states,
        'moves': game.moves,
        'phase': game.phase,
        'win': game.is_win(),
        'lose':game.is_lose(),
    }
    return JsonResponse(response)


def get_game(request):
    """Retrieve the current :class:`GameBoard` from the session.

    If no game is stored, a new one is created. The resulting game state is
    written back to the session to ensure persistence between requests.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request containing the session.

    Returns
    -------
    GameBoard
        The game board representing the current game state.
    """
def get_game(request):
    """Retrieve or create the current GameBoard."""
    data = request.session.get(SESSION_KEY)
    if data:
        game = GameBoard(data)
    else:
        level = request.session.get('difficulty', 'facil')
        levels = {
            'facil': 3,
            'medio': 6,
            'dificil': 12
        }
        num_pairs = levels.get(level, 3)
        game = GameBoard.new_game(num_pairs)
    
    request.session[SESSION_KEY] = game.to_dict()
    return game



def index(request):
    """Render the main game page with the current board state."""
    game = get_game(request)
    context = {
        'game': game,
    }
    return render(request, 'memory_game/index.html', context)


def flip_card(request, index):
    """Flip a card at the given ``index`` and return the updated game state."""
    game = get_game(request)
    mismatch = False
    if index == -1:
        # ``-1`` is used by the frontend to resolve a mismatch after a delay
        game.flip(None)
    else:
        mismatch = game.flip(index)

    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': game.states,
        'moves': game.moves,
        'win': game.is_win(),
        'lose': game.is_lose(),
        'mismatch': mismatch,
        'phase': game.phase,
    }
    return JsonResponse(response)


def restart_game(request):
    """Clear the current game from the session and redirect to ``index``."""
    if SESSION_KEY in request.session:
        del request.session[SESSION_KEY]
    return redirect(reverse('index'))


def start_memorizing(request):
    """Transition the game into the memorizing phase."""
    game = get_game(request)
    game.start_memorizing()
    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': [1] * len(game.cards),  # Show all cards
        'moves': game.moves,
        'phase': game.phase,
        'win': False,
        'lose':False,
    }
    return JsonResponse(response)


def start_playing(request):
    """Transition the game into the playing phase."""
    game = get_game(request)
    game.start_playing()
    request.session[SESSION_KEY] = game.to_dict()
    response = {
        'cards': game.cards,
        'states': game.states,
        'moves': game.moves,
        'phase': game.phase,
        'win': False,
        'lose':False,
    }
    return JsonResponse(response)
