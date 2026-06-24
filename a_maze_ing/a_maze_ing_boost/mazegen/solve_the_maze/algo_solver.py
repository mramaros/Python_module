#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   algo_solver.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 17:19:18 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/12 10:51:55 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from ..generate_cellule.class_cell import Cell
from ..generate_cellule import get_cell
import random


def solver_back(
    all_cell: list[Cell],
    WIDTH: int,
    ENTRY_X: int,
    ENTRY_Y: int,
    EXIT_X: int,
    EXIT_Y: int,
    OUTLINE_THICKNESS: int,
    CELL_SIZE: int,
) -> list[tuple[int, int]]:
    stack = []
    visited = set()

    ent_x = (ENTRY_X - OUTLINE_THICKNESS) // CELL_SIZE
    ent_y = (ENTRY_Y - OUTLINE_THICKNESS) // CELL_SIZE
    ext_x = (EXIT_X - OUTLINE_THICKNESS) // CELL_SIZE
    ext_y = (EXIT_Y - OUTLINE_THICKNESS) // CELL_SIZE
    end = (ent_x, ent_y)

    stack.append((ent_x, ent_y))
    visited.add((ent_x, ent_y))

    while stack and end != (ext_x, ext_y):
        x, y = stack[-1]
        current = get_cell(all_cell, x, y, WIDTH)
        end = (current.x, current.y)
        options = []

        if current.wall[0] == 0 and (x, y - 1) not in visited:
            options.append((x, y - 1))
        if current.wall[1] == 0 and (x + 1, y) not in visited:
            options.append((x + 1, y))
        if current.wall[2] == 0 and (x, y + 1) not in visited:
            options.append((x, y + 1))
        if current.wall[3] == 0 and (x - 1, y) not in visited:
            options.append((x - 1, y))

        if options and end != (ext_x, ext_y):
            next_x, next_y = random.choice(options)
            stack.append((next_x, next_y))
            visited.add((next_x, next_y))

        else:
            stack.pop()

    if len(stack) > 0:
        stack.pop(0)
    return stack
