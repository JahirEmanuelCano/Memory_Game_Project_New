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
        if data:
            # Restore saved state from the session
            self.cards = data.get('cards', [])
            self.states = data.get('states', [])
            self.moves = data.get('moves', 0)
            self.phase = data.get('phase', 'setup')  # setup, memorizing, playing
            self.start_time = data.get('start_time', None)
        else:
            self.new_game()

    def new_game(self):
        """Initialize a new shuffled board in ``setup`` phase."""
        pairs = list(range(8)) * 2
        random.shuffle(pairs)
        self.cards = pairs
        # 0 = hidden, 1 = flipped, 2 = matched
        self.states = [0] * len(self.cards)
        self.moves = 0
        self.phase = 'setup'  # setup, memorizing, playing
        self.start_time = None

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
