#!/usr/bin/env python3


class Cell:
    def __init__(self, x: int, y: int, wall: list[list[int]]) -> None:
        self.x = x
        self.y = y
        self.wall = wall
        self.value = (
            self.wall[3][0] * 8
            + self.wall[2][0] * 4
            + self.wall[1][0] * 2
            + self.wall[0][0] * 1
        )

    def hex_char(self) -> str:
        self.value = (
            self.wall[3][0] * 8
            + self.wall[2][0] * 4
            + self.wall[1][0] * 2
            + self.wall[0][0] * 1
        )
        if self.value < 10:
            return str(self.value)
        return "ABCDEF"[self.value - 10]
