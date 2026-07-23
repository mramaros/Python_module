#!/usr/bin/env python3


from .generate_cellule import Cell
import random
from typing import Any


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry_xy: tuple[int, int],
        exit_xy: tuple[int, int],
        the_seed: str | None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry_xy
        self.exit = exit_xy

        self.the_seed = the_seed
        random.seed(self.the_seed)

        self.all_cell: list[Cell] = []
        self.all_isolated: list[Any] = []
        self.solve: list[tuple[int, int]] = []

    def create_all_cells(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.all_cell.append(
                    Cell(j, i, [[1, True], [1, True], [1, True], [1, True]])
                )

    def isolated_cells(self) -> list[tuple[int, int]]:
        self.all_isolated.extend(
            [
                (self.width // 2 - 3, self.height // 2 - 2),
                (self.width // 2 - 3, self.height // 2 - 1),
                (self.width // 2 - 3, self.height // 2),
                (self.width // 2 - 2, self.height // 2),
                (self.width // 2 - 1, self.height // 2),
                (self.width // 2 - 1, self.height // 2 + 1),
                (self.width // 2 - 1, self.height // 2 + 2),
                (self.width // 2 + 3, self.height // 2 + 2),
                (self.width // 2 + 2, self.height // 2 + 2),
                (self.width // 2 + 1, self.height // 2 + 2),
                (self.width // 2 + 1, self.height // 2 + 1),
                (self.width // 2 + 1, self.height // 2),
                (self.width // 2 + 2, self.height // 2),
                (self.width // 2 + 3, self.height // 2),
                (self.width // 2 + 3, self.height // 2 - 1),
                (self.width // 2 + 3, self.height // 2 - 2),
                (self.width // 2 + 2, self.height // 2 - 2),
                (self.width // 2 + 1, self.height // 2 - 2),
            ]
        )
        return list(self.all_isolated)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.all_cell[y * self.width + x]

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        n = []

        if x > 0:
            n.append((x - 1, y))
        if x < self.width - 1:
            n.append((x + 1, y))
        if y > 0:
            n.append((x, y - 1))
        if y < self.height - 1:
            n.append((x, y + 1))
        return n

    def generated_maze_dfs(self) -> list[tuple[int, int]]:

        stack = []
        visited = set()
        all_path = []

        begin = self.entry
        stack.append(begin)
        visited.add(begin)
        all_path.append(begin)

        while stack:
            x, y = stack[-1]
            current = self.get_cell(x, y)

            options = []
            for next_x, next_y in self.neighbors(x, y):
                if self.width >= 9 and self.height >= 8:
                    if (next_x, next_y) not in self.all_isolated:
                        if (next_x, next_y) not in visited:
                            options.append((next_x, next_y))
                else:
                    if (next_x, next_y) not in visited:
                        options.append((next_x, next_y))

            if options:
                next_x, next_y = random.choice(options)
                the_next = self.get_cell(next_x, next_y)

                if next_y == y - 1:
                    current.wall[0][0] = 0
                    the_next.wall[2][0] = 0

                elif next_x == x + 1:
                    current.wall[1][0] = 0
                    the_next.wall[3][0] = 0

                elif next_y == y + 1:
                    current.wall[2][0] = 0
                    the_next.wall[0][0] = 0

                elif next_x == x - 1:
                    current.wall[3][0] = 0
                    the_next.wall[1][0] = 0

                stack.append((next_x, next_y))
                visited.add((next_x, next_y))
                all_path.append((next_x, next_y))
            else:
                stack.pop()

        return all_path

    def generated_maze_prim_s(self) -> list[tuple[int, int]]:
        frontier = []
        visited = set()
        all_path = []

        center_x: int = self.width // 2
        center_y: int = self.height // 2
        begin = (center_x, center_y)

        visited.add(begin)
        all_path.append(begin)
        for next_x, next_y in self.neighbors(begin[0], begin[1]):
            frontier.append((begin[0], begin[1], next_x, next_y))

        while frontier:
            x1, y1, x2, y2 = random.choice(frontier)
            frontier.remove((x1, y1, x2, y2))

            if (x2, y2) not in visited:
                if self.width >= 9 and self.height >= 8:
                    if (x2, y2) in self.all_isolated:
                        continue

                visited.add((x2, y2))
                all_path.append((x2, y2))

                current = self.get_cell(x1, y1)
                new = self.get_cell(x2, y2)

                if y2 == y1 - 1:
                    current.wall[0][0] = 0
                    new.wall[2][0] = 0

                elif x2 == x1 + 1:
                    current.wall[1][0] = 0
                    new.wall[3][0] = 0

                elif y2 == y1 + 1:
                    current.wall[2][0] = 0
                    new.wall[0][0] = 0

                elif x2 == x1 - 1:
                    current.wall[3][0] = 0
                    new.wall[1][0] = 0

                for nx, ny in self.neighbors(x2, y2):
                    if (nx, ny) not in visited:
                        frontier.append((x2, y2, nx, ny))

        return all_path

    def is_open_3x3(self, x0: int, y0: int) -> bool:
        # murs horizontal (2, 0)
        for x in range(x0, x0 + 3):
            for y in range(y0, y0 + 2):
                c1 = self.get_cell(x, y)
                c2 = self.get_cell(x, y + 1)
                if c1.wall[2][0] or c2.wall[0][0]:
                    return False

        # murs vertical (3, 1)
        for y in range(y0, y0 + 3):
            for x in range(x0, x0 + 2):
                c1 = self.get_cell(x, y)
                c2 = self.get_cell(x + 1, y)
                if c1.wall[1][0] or c2.wall[3][0]:
                    return False

        return True

    def imperfect_maze(self, a_cell: Cell) -> None:
        destroy_or_not = 0.15

        all_walls = {
            "N": (0, -1, 0, 2),
            "E": (1, 0, 1, 3),
            "S": (0, 1, 2, 0),
            "W": (-1, 0, 3, 1),
        }
        if self.width >= 9 and self.height >= 8:
            if (a_cell.x, a_cell.y) in self.all_isolated:
                return

        nbr_1 = sum(wall[0] for wall in a_cell.wall)

        if random.random() < destroy_or_not or nbr_1 > 2:
            options = []
            for direction, (
                tx,
                ty,
                the_wall,
                other_wall,
            ) in all_walls.items():
                nx = a_cell.x + tx
                ny = a_cell.y + ty

                if self.width >= 9 and self.height >= 8:
                    if (nx, ny) in self.all_isolated:
                        continue

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    the_neighbor = self.get_cell(nx, ny)

                    if (
                        a_cell.wall[the_wall][0]
                        and the_neighbor.wall[other_wall][0]
                    ):
                        options.append((the_wall, other_wall, the_neighbor))

            if len(options) == 0:
                return

            the_wall, other_wall, the_neighbor = random.choice(options)
            a_cell.wall[the_wall][0] = 0
            a_cell.wall[the_wall][1] = False
            the_neighbor.wall[other_wall][0] = 0
            the_neighbor.wall[other_wall][1] = False

            for x in range(
                max(0, a_cell.x - 2), min(self.width - 3, a_cell.x) + 1
            ):
                for y in range(
                    max(0, a_cell.y - 2), min(self.height - 3, a_cell.y) + 1
                ):
                    if self.is_open_3x3(x, y):
                        a_cell.wall[the_wall][0] = 1
                        a_cell.wall[the_wall][1] = True
                        the_neighbor.wall[other_wall][0] = 1
                        the_neighbor.wall[other_wall][1] = True

    def solver_dfs(
        self,
        entry_x: int,
        entry_y: int,
        exit_x: int,
        exit_y: int,
        outline_thickness: int,
        CELL_SIZE: int,
    ) -> list[tuple[int, int]]:

        stack = []
        visited = set()

        start_x = (entry_x - outline_thickness) // CELL_SIZE
        start_y = (entry_y - outline_thickness) // CELL_SIZE
        end_x = (exit_x - outline_thickness) // CELL_SIZE
        end_y = (exit_y - outline_thickness) // CELL_SIZE

        stack.append((start_x, start_y))
        visited.add((start_x, start_y))

        while stack:
            x, y = stack[-1]

            if (x, y) == (end_x, end_y):
                self.solve = stack
                return list(stack)

            current = self.get_cell(x, y)
            options = []

            if current.wall[0][0] == 0 and (x, y - 1) not in visited:
                options.append((x, y - 1))

            if current.wall[1][0] == 0 and (x + 1, y) not in visited:
                options.append((x + 1, y))

            if current.wall[2][0] == 0 and (x, y + 1) not in visited:
                options.append((x, y + 1))

            if current.wall[3][0] == 0 and (x - 1, y) not in visited:
                options.append((x - 1, y))

            if options:
                next_cell = random.choice(options)
                stack.append(next_cell)
                visited.add(next_cell)
            else:
                stack.pop()

        return []

    def solver_bfs(
        self,
        entry_x: int,
        entry_y: int,
        exit_x: int,
        exit_y: int,
        outline_thickness: int,
        cell_size: int,
    ) -> list[tuple[int, int]]:

        the_file = []
        his_parents: dict[tuple[int, int], tuple[int, int]] = {}
        visiset = set()

        start_x = (entry_x - outline_thickness) // cell_size
        start_y = (entry_y - outline_thickness) // cell_size
        end_x = (exit_x - outline_thickness) // cell_size
        end_y = (exit_y - outline_thickness) // cell_size

        the_file.append((start_x, start_y))
        visiset.add((start_x, start_y))

        while the_file:
            x, y = the_file.pop(0)

            if (x, y) == (end_x, end_y):
                path = []
                current = (end_x, end_y)

                while current != (start_x, start_y):
                    path.append(current)
                    current = his_parents[current]
                path.append((start_x, start_y))
                path.reverse()
                return path

            for nx, ny in self.neighbors(x, y):
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in self.all_isolated and (
                        nx,
                        ny,
                    ) not in visiset:
                        tx = nx - x
                        ty = ny - y
                        the_current = self.get_cell(x, y)
                        the_next = self.get_cell(nx, ny)
                        ok = False

                        if (tx, ty) == (0, -1):
                            if (
                                not the_current.wall[0][0]
                                and not the_next.wall[2][0]
                            ):
                                ok = True

                        elif (tx, ty) == (1, 0):
                            if (
                                not the_current.wall[1][0]
                                and not the_next.wall[3][0]
                            ):
                                ok = True

                        elif (tx, ty) == (0, 1):
                            if (
                                not the_current.wall[2][0]
                                and not the_next.wall[0][0]
                            ):
                                ok = True

                        elif (tx, ty) == (-1, 0):  # gauche
                            if (
                                not the_current.wall[3][0]
                                and not the_next.wall[1][0]
                            ):
                                ok = True

                        if ok:
                            visiset.add((nx, ny))
                            his_parents[(nx, ny)] = (x, y)
                            the_file.append((nx, ny))
        return []
