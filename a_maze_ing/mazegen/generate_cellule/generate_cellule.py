#!/usr/bin/env python3


from typing import List
from .class_cell import Cell


def get_cell(all_cell: List[Cell], x: int, y: int, WIDTH: int) -> Cell:
    """Retourne la cellule aux coordonnées (x,y) dans la liste linéaire."""
    return all_cell[y * WIDTH + x]
