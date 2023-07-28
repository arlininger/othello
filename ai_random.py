"""Provides a class for a random AI"""

import random

class RandomAI:
    """Implements a random ai"""

    def get_move(self, board):
        """Return the current move"""
        return random.choice(board.current_possible_moves)
