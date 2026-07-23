#!/usr/bin/env python3


def solver_in_nesw(solver: list[tuple[int, int]]) -> list[str]:
    nesw = []
    for i in range(len(solver) - 1):
        x = solver[i + 1][0] - solver[i][0]
        y = solver[i + 1][1] - solver[i][1]
        if x == 0 and y == -1:
            nesw.append("N")
        elif x == 1 and y == 0:
            nesw.append("E")
        elif x == 0 and y == 1:
            nesw.append("S")
        elif x == -1 and y == 0:
            nesw.append("W")
    return nesw
