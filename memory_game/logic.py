"""Core game logic for the Memory Game with images."""

import random

class GameBoard:
    """Representation of the memory game board and its current state."""

    # Pool de imágenes disponibles (puedes cambiar por rutas de imágenes reales)
    IMAGE_POOL = [
        '🐶', '🐱', '🐭', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁',
        '🐮', '🐷', '🐸', '🐵', '🐧', '🦋', '🐝', '🐞', '🦆', '🦅',
        '🌺', '🌸', '🌼', '🌻', '🌷', '🌹', '🌿', '🍀', '🌳', '🌲'
    ]
    
    # Si prefieres usar rutas de imágenes reales, usa esto:
    # IMAGE_POOL = [
    #     '/static/images/dog.png',
    #     '/static/images/cat.png',
    #     '/static/images/mouse.png',
    #     # ... más imágenes
    # ]

    def __init__(self, data=None):
        """Create a new board or restore one from ``data``."""
        self.errors = 0
        #cantErrores = 0
        if data:
            # Restore saved state from the session
            self.cards = data.get('cards', [])
            self.states = data.get('states', [])
            self.moves = data.get('moves', 0)
            self.phase = data.get('phase', 'setup')
            self.start_time = data.get('start_time', None)
        else:
            self._init_board(8)

    def _init_board(self, num_pairs):
        """Initialize board with image pairs."""
        # Selecciona imágenes aleatorias del pool
        selected_images = random.sample(self.IMAGE_POOL, num_pairs)
        
        # Crea pares duplicando cada imagen
        pairs = selected_images * 2
        random.shuffle(pairs)
        
        self.cards = pairs
        # 0 = oculta, 1 = volteada, 2 = emparejada
        self.states = [0] * len(self.cards)
        self.moves = 0
        self.phase = 'setup'
        self.start_time = None

    @classmethod
    def new_game(cls, num_pairs=8):
        """Crea y devuelve un nuevo juego con el número de pares especificado."""
        instance = cls()
        instance._init_board(num_pairs)
        return instance

    def flip(self, index):
        """Flip a card and evaluate if a pair is found."""
        if index is None:
            self._resolve_mismatch()
            return False

        if not self.can_flip():
            return False

        if index < 0 or index >= len(self.cards):
            return False

        if self.states[index] != 0:
            return False

        if len(self._uncovered_indices()) == 2:
            return False

        self.states[index] = 1
        mismatch = False
        uncovered = self._uncovered_indices()
        if len(uncovered) == 2:
            i, j = uncovered
            # Comparar las imágenes en lugar de números
            if self.cards[i] == self.cards[j]:
                self.states[i] = self.states[j] = 2
                mismatch = False
            else:
                mismatch = True
                self.errors += 1
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
        return self.errors >= 1
    
    def start_memorizing(self):
        """Begin the memorizing phase showing all cards."""
        self.phase = 'memorizing'
        import time
        self.start_time = time.time()
    
    def start_playing(self):
        """Begin the playing phase hiding all cards and resetting moves."""
        self.phase = 'playing'
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
