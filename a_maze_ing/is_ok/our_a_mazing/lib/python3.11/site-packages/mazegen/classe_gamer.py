#!/usr/bin/env python3


class GameState:
    def __init__(self, entry_xy: tuple[int, int], exit_xy: tuple[int, int]):
        self.pos = entry_xy
        self.exit_pos = exit_xy
        self.play_or_not = False
