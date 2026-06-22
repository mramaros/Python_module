# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generate_maze.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <mramaros@student.42antananarivo  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/09 06:44:35 by mramaros          #+#    #+#              #
#    Updated: 2026/06/09 06:44:36 by mramaros         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Module de génération de labyrinthe.
Contient les fonctions indépendantes de la logique d'affichage.
"""
import random
from typing import List, Tuple, Set
from mazegen.generate_cellule import Cell


def get_cell(all_cell, x: int, y: int, WIDTH: int):
    """Retourne la cellule aux coordonnées (x,y) dans la liste linéaire.

    `WIDTH` doit être fourni pour calculer l'index linéaire.
    """
    return all_cell[y * WIDTH + x]


def neighbors(WIDTH: int, HEIGHT: int, x: int, y: int) -> List[Tuple[int, int]]:
    '''
    Retourne une liste de coordonnées (x,y) des cellules voisines de (x,y) dans la grille.
    Les voisins sont dans les directions haut, bas, gauche, droite (pas de diagonales).
    '''
    n = []
    if x > 0:
        n.append((x - 1, y))
    if x < WIDTH - 1:
        n.append((x + 1, y))
    if y > 0:
        n.append((x, y - 1))
    if y < HEIGHT - 1:
        n.append((x, y + 1))
    return n



def generated_maze_back(all_cell: list[Cell], isoler: set[tuple[int, int]], WIDTH: int, HEIGHT: int) -> list[tuple[int, int]]:
    stack = []
    visited = set()
    list_anime = []

    begin = (0, 0)
    stack.append(begin)
    visited.add(begin)
    list_anime.append(begin)

    while stack:
        x, y = stack[-1]
        current = get_cell(all_cell, x, y, WIDTH)

        options = []
        for next_x, next_y in neighbors(WIDTH, HEIGHT, x, y):
            if (next_x, next_y) not in visited and (next_x, next_y) not in isoler:
                options.append((next_x, next_y))

        if options:
            next_x, next_y = random.choice(options)
            the_next = get_cell(all_cell, next_x, next_y, WIDTH)

            if next_y == y - 1:
                current.wall[0] = 0
                the_next.wall[2] = 0

            elif next_x == x + 1:
                current.wall[1] = 0
                the_next.wall[3] = 0

            elif next_y == y + 1:
                current.wall[2] = 0
                the_next.wall[0] = 0

            elif next_x == x - 1:
                current.wall[3] = 0
                the_next.wall[1] = 0

            stack.append((next_x, next_y))
            visited.add((next_x, next_y))
            list_anime.append((next_x, next_y))

        else:
            stack.pop()

    return list_anime


def generated_maze(all_cell, isolated: Set[Tuple[int, int]], WIDTH: int, HEIGHT: int) -> None:
    """Génère le labyrinthe en modifiant `all_cell` en place.

    `all_cell` doit être une liste linéaire de cellules indexée par y*WIDTH + x.
    `isolated` est un ensemble de coordonnées (x,y) à ne pas visiter.
    """
    stack = []
    visited = set()

    begin = (0, 0)
    stack.append(begin)
    visited.add(begin)

    while stack:
        x, y = stack[-1]
        current = get_cell(all_cell, x, y, WIDTH)

        options = []
        for next_x, next_y in neighbors(WIDTH, HEIGHT, x, y):
            if (next_x, next_y) not in visited and (next_x, next_y) not in isolated:
                options.append((next_x, next_y))

        if options:
            next_x, next_y = random.choice(options)
            the_next = get_cell(all_cell, next_x, next_y, WIDTH)

            if next_y == y - 1:
                current.wall[0] = 0
                the_next.wall[2] = 0

            elif next_x == x + 1:
                current.wall[1] = 0
                the_next.wall[3] = 0

            elif next_y == y + 1:
                current.wall[2] = 0
                the_next.wall[0] = 0

            elif next_x == x - 1:
                current.wall[3] = 0
                the_next.wall[1] = 0

            stack.append((next_x, next_y))
            visited.add((next_x, next_y))

        else:
            stack.pop()
