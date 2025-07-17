"""Core game logic for the Memory Game."""

import random

class GameBoard:
    """Representation of the memory game board and its current state."""

    def __init__(self, data=None):
        """Create a new board or restore one from ``data``.

        Parameters
        ----------
        data : dict, optional
            Serialized board state previously returned by :meth:`to_dict`.
        """
        self.errors = 0

        if data:
            # Restore saved state from the session
            self.cards = data.get('cards', [])
            self.states = data.get('states', [])
            self.moves = data.get('moves', 0)
            self.phase = data.get('phase', 'setup')  # setup, memorizing, playing
            self.start_time = data.get('start_time', None)
        else:
            # Si no se provee data, inicializa con el valor por defecto.
            self._init_board(8)  # Por defecto se crean 8 pares (16 cartas)

    def _init_board(self, num_pairs):

        # Genera los pares (los números van del 1 al num_pairs)
        pairs = list(range(1, num_pairs + 1)) * 2
        random.shuffle(pairs)
        self.cards = pairs
        # 0 = oculta, 1 = volteada, 2 = emparejada
        self.states = [0] * len(self.cards)
        self.moves = 0
        self.phase = 'setup'  # setup, memorizing, playing
        self.start_time = None

    
    @classmethod
    def new_game(cls, num_pairs=8):
        """Crea y devuelve un nuevo juego con el número de pares especificado.

        Parámetros:
            num_pairs (int): Número de pares. Ej.: 4 (fácil), 8 (medio), 12 (difícil).

        Retorna:
            GameBoard: Una instancia nueva inicializada.
        """
        
        instance = cls()
        instance._init_board(num_pairs)
        return instance

    def flip(self, index):
        """Flip a card and evaluate if a pair is found.

        Parameters
        ----------
        index : int or None
            Index of the card to flip. ``None`` signals that a mismatch should
            be resolved by hiding the previously flipped cards.

        Returns
        -------
        bool
            ``True`` if the flipped pair does not match, ``False`` otherwise.
        """
        
        if index is None:
            # Called after a delay to hide unmatched cards
            self._resolve_mismatch()
            return False

        # Only allow flipping in playing phase
        if not self.can_flip():
            return False

        if index < 0 or index >= len(self.cards):
            return False

        if self.states[index] != 0:
            return False

        if len(self._uncovered_indices()) == 2:
            return False

        # Reveal the selected card
        self.states[index] = 1
        mismatch = False
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            if self.cards[i] == self.cards[j]:
                self.states[i] = self.states[j] = 2
                mismatch = False
            else:
                mismatch = True
                self.errors +=1
            self.moves += 1
        return mismatch

    def _resolve_mismatch(self):
        """Hide the two currently flipped cards if they do not match."""
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            if self.cards[i] != self.cards[j]:
                self.states[i] = self.states[j] = 0

    def _uncovered_indices(self):
        """Return indices of cards that are currently flipped but not matched."""
        return [i for i, s in enumerate(self.states) if s == 1]

    def is_win(self):
        """Return ``True`` if all cards have been matched."""
        return all(s == 2 for s in self.states)
    
    def is_lose(self):
       return self.errors>=1
    
    def start_memorizing(self):
        """Begin the memorizing phase showing all cards."""
        self.phase = 'memorizing'
        import time
        self.start_time = time.time()
    
    def start_playing(self):
        """Begin the playing phase hiding all cards and resetting moves."""
        self.phase = 'playing'
        # Reset all cards to hidden state
        self.states = [0] * len(self.cards)
        self.moves = 0
    
    def can_flip(self):
        """Return ``True`` if cards may be flipped in the current phase."""
        return self.phase == 'playing'

    def to_dict(self):
        """Serialize the board to a dictionary for storing in the session."""
        return {
            'cards': self.cards,
            'states': self.states,
            'moves': self.moves,
            'phase': self.phase,
            'start_time': self.start_time,
        }
