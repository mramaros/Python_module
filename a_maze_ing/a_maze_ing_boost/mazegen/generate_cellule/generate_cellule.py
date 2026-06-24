# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generate_cellule.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <mramaros@student.42antananarivo  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/09 06:44:11 by mramaros          #+#    #+#              #
#    Updated: 2026/06/09 06:44:14 by mramaros         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
Gestion des cellules du labyrinthe.
Contient la classe `Cell`, la création de la grille linéaire et l'accès par coordonnées.
"""

from typing import List
from .class_cell import Cell


def get_cell(all_cell: List[Cell], x: int, y: int, WIDTH: int) -> Cell:
    """Retourne la cellule aux coordonnées (x,y) dans la liste linéaire."""
    return all_cell[y * WIDTH + x]


def create_all_cells(WIDTH: int, HEIGHT: int) -> List[Cell]:
    """
    Créer la liste de toutes les cellules initialisées avec tous les murs.

    Retourne une liste de `WIDTH * HEIGHT` instances `Cell`.
    """
    new: List[Cell] = []
    for i in range(HEIGHT):  # ligne (y)
        for j in range(WIDTH):  # colonne (x)
            new.append(Cell(j, i, [1, 1, 1, 1]))
    return new
