"""Provides a class for a Non-AI"""

class NoAI:
    """Implements a non-AI ai"""

    current_move = None

    def get_move(self, game):
        """Return the current move"""
        ret = self.current_move
        self.current_move = None
        return ret

    def set_move(self,move):
        """Set the current move"""
        self.current_move = move
