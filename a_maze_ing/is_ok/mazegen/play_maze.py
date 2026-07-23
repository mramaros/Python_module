#!/usr/bin/env python3
"""Module defining the interactive gameplay mechanics."""

from typing import Any, Protocol
from .classe_maze_generator import MazeGenerator
from .generate_cellule import Cell
from .renderer import MazeMlx

KEY_LEFT = 65361
KEY_UP = 65362
KEY_RIGHT = 65363
KEY_DOWN = 65364


class GameStateLike(Protocol):
    """
    Structural stand-in for the game state protocol.

    Attributes:
        pos (tuple[int, int]): Current coordinates of the player.
        play_or_not (bool): Flag determining if the game is playable.
    """

    pos: tuple[int, int]
    play_or_not: bool


def play_the_maze(
    keycode: int,
    all_stat: dict[str, Any],
    class_maze: MazeGenerator,
    the_window: MazeMlx,
    all_cell: list[Cell],
    isoler: list[tuple[int, int]],
    state: GameStateLike,
    true_entry: tuple[int, int],
    tuple_exit: tuple[int, int],
    WIDTH: int,
    HEIGHT: int,
) -> None:
    """
    Process player movement and handle game completion logic.

    Args:
        keycode (int): The directional keycode mapped to an arrow key.
        all_stat (dict[str, Any]): Dictionary containing global app state.
        class_maze (MazeGenerator): The instantiated maze class.
        the_window (MazeMlx): The instantiated MLX renderer.
        all_cell (list[Cell]): List of all maze cells.
        isoler (list[tuple[int, int]]): List of isolated cell coordinates.
        state (GameStateLike): The current player's game state.
        true_entry (tuple[int, int]): Initial starting point coordinates.
        tuple_exit (tuple[int, int]): Finish point coordinates.
        WIDTH (int): Total width in cells.
        HEIGHT (int): Total height in cells.
    """

    space = "    "
    space1 = "                  "
    congratulation = [
        f"{space} ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ ████████╗"
        "██╗   ██╗██╗      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗",
        f"{space}██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝"
        "██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝",
        f"{space}██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║   ██║   "
        "██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗",
        f"{space}██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║   ██║   "
        "██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║",
        f"{space}╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║   ██║   "
        "╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║",
        f"{space} ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "
        " ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝",
        "",
        f"{space1}                                  🎉 Congratulations! 🎉",
    ]

    x, y = state.pos
    direction = ""
    if keycode == KEY_UP:  # Up
        the_next = (x, y - 1)
        direction = "N"

    elif keycode == KEY_RIGHT:  # right
        the_next = (x + 1, y)
        direction = "E"

    elif keycode == KEY_DOWN:  # down
        the_next = (x, y + 1)
        direction = "S"

    elif keycode == KEY_LEFT:  # left
        the_next = (x - 1, y)
        direction = "W"

    else:
        return

    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        if 0 <= the_next[0] < WIDTH and 0 <= the_next[1] < HEIGHT:
            if (x, y) not in isoler and the_next not in isoler:

                ok = False
                A = class_maze.get_cell(x, y)
                B = class_maze.get_cell(the_next[0], the_next[1])

                if direction == "N":
                    if A.wall[0][0] == 0 and B.wall[2][0] == 0:
                        ok = True

                elif direction == "E":
                    if A.wall[1][0] == 0 and B.wall[3][0] == 0:
                        ok = True

                elif direction == "S":
                    if A.wall[2][0] == 0 and B.wall[0][0] == 0:
                        ok = True

                elif direction == "W":
                    if A.wall[3][0] == 0 and B.wall[1][0] == 0:
                        ok = True

                if ok:
                    state.pos = the_next
                    the_window.fill_cell(all_stat, x, y, 0xFF000000)
                    the_window.fill_cell(
                        all_stat, the_next[0], the_next[1], 0xFF00FF00
                    )

        if state.pos == tuple_exit:
            state.play_or_not = False
            print("\n\n\n")
            for line in congratulation:
                print(line)
    return
