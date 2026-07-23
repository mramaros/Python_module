#!/usr/bin/env python3


class GameState:
    """
    Represent the current state of the game.

    Attributes:
        pos (tuple[int, int]): The current player position (x, y).
        exit_pos (tuple[int, int]): The target exit position (x, y).
        play_or_not (bool): Flag indicating if the maze is in play mode.
    """
    def __init__(self, entry_xy: tuple[int, int], exit_xy: tuple[int, int]):
        """
        Initialize the game state with entry and exit coordinates.

        Args:
            entry_xy (tuple[int, int]): The starting (x, y) coordinates.
            exit_xy (tuple[int, int]): The finishing (x, y) coordinates.
        """
        self.pos = entry_xy
        self.exit_pos = exit_xy
        self.play_or_not = False
