"""
Random Baseline Agent for Tic-Tac-Toe.
                  (توسعه دهنده علی احمدی)
"""

import numpy as np


class RandomBaselineAgent:
    """
    A pure-random baseline agent.
    """

    def __init__(self, player=1, seed=None):
        if player not in (1, -1):
            raise ValueError("player must be 1 (X) or -1 (O).")

        self.player = player
        self.rng = np.random.default_rng(seed)

    def select_action(self, env):
        """
        Select one legal action uniformly at random.
        """

        legal_actions = env.get_legal_actions()

        if not legal_actions:
            return None

        return int(self.rng.choice(legal_actions))