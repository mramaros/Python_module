#!/usr/bin/env python3


from typing import List
from .class_cell import Cell as Cell


def get_cell(all_cell: List[Cell], x: int, y: int, WIDTH: int) -> Cell:
    return all_cell[y * WIDTH + x]
