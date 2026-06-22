# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    class_cell.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <mramaros@student.42antananarivo  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/09 06:43:59 by mramaros          #+#    #+#              #
#    Updated: 2026/06/09 06:44:16 by mramaros         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from typing import List
from mlx import mlx

class Cell:
    def __init__(self, x: int, y: int, wall: List[int]) -> None:
        self.x = x
        self.y = y
        self.wall = wall
        self.value = (
            self.wall[3] * 8
            + self.wall[2] * 4
            + self.wall[1] * 2
            + self.wall[0] * 1
        )

    def draw(self) -> None:
        print(self.hex_char(), end="")

    def hex_char(self) -> str:
        self.value = (
            self.wall[3] * 8
            + self.wall[2] * 4
            + self.wall[1] * 2
            + self.wall[0] * 1
        )
        if self.value < 10:
            return str(self.value)
        return "ABCDEF"[self.value - 10]