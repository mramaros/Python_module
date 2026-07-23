#!/usr/bin/env python3


from .generate_cellule import Cell, get_cell
from .generate_maze import isolated_cells
from typing import Any
import sys

try:
    from mlx import Mlx
except Exception:
    sys.exit("The module mlx could not be found")


class MazeMlx:
    def __init__(
        self,
        cols: int,
        rows: int,
        width: int,
        height: int,
        cell_size: int,
        outline_thickness: int,
    ) -> None:
        self.cols = cols
        self.rows = rows
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.outline_thickness = outline_thickness

        the_width = (self.cols - self.outline_thickness) // self.cell_size
        the_height = (self.rows - self.outline_thickness) // self.cell_size
        self.isoler = isolated_cells(the_width, the_height)

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(
            self.mlx_ptr, cols + 30, rows + 80, "A-Maze-ing"
        )
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, cols, rows)

        self.data, self.bpp, self.sl, self.fmt = self.mlx.mlx_get_data_addr(
            self.img
        )

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            offset = y * self.sl + x * (self.bpp // 8)
            self.data[offset: offset + 4] = color.to_bytes(4, "little")

    def put_pixel_all_image(self, old_color: int, new_color: int) -> None:
        old = old_color.to_bytes(4, "little")
        new = new_color.to_bytes(4, "little")

        for i in range(0, len(self.data), 4):
            if self.data[i: i + 4] == old:
                self.data[i: i + 4] = new

    def clean_all(self) -> None:
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win)
        self.mlx.mlx_release(self.mlx_ptr)

    def draw_line_h(
        self, x0: int, y0: int, length: int, color: int, thickness: int = 1
    ) -> None:
        for t in range(thickness):
            for dx in range(length):
                self.put_pixel(x0 + dx, y0 + t, color)

    def draw_line_v(
        self, x0: int, y0: int, length: int, color: int, thickness: int = 1
    ) -> None:
        for t in range(thickness):
            for dy in range(length):
                self.put_pixel(x0 + t, y0 + dy, color)

    def delet_line_h(
        self,
        x0: int,
        y0: int,
        length: int,
        thickness: int = 1,
        perfect: bool = True,
    ) -> None:
        for t in range(thickness):
            if perfect:
                for dx in range(thickness, length):
                    self.put_pixel(x0 + dx, y0 + t, 0xFF000000)
            else:
                for dx in range(length):
                    self.put_pixel(x0 + dx, y0 + t, 0xFF000000)

    def delet_line_v(
        self,
        x0: int,
        y0: int,
        length: int,
        thickness: int = 1,
        perfect: bool = True,
    ) -> None:
        for t in range(thickness):
            if perfect:
                for dy in range(thickness, length):
                    self.put_pixel(x0 + t, y0 + dy, 0xFF000000)
            else:
                for dy in range(length):
                    self.put_pixel(x0 + t, y0 + dy, 0xFF000000)

    def color_entry_and_exit(
        self, entry_x: int, entry_y: int, exit_x: int, exit_y: int
    ) -> None:
        for x in range(
            entry_x, entry_x + self.cell_size - self.outline_thickness
        ):
            for y in range(
                entry_y, entry_y + self.cell_size - self.outline_thickness
            ):
                self.put_pixel(x, y, 0x1100FF00)
        for x in range(
            exit_x, exit_x + self.cell_size - self.outline_thickness
        ):
            for y in range(
                exit_y, exit_y + self.cell_size - self.outline_thickness
            ):
                self.put_pixel(x, y, 0x11FF0000)

    def color_content_solver(
        self,
        all_cell: list[Cell],
        his_x: int,
        his_y: int,
        solver_slice: list[tuple[int, int]],
        color: int,
    ) -> None:
        center_x = (
            his_x * self.cell_size
            + self.outline_thickness
            + (self.cell_size - self.outline_thickness) // 2
        )
        center_y = (
            his_y * self.cell_size
            + self.outline_thickness
            + (self.cell_size - self.outline_thickness) // 2
        )

        if len(solver_slice) > 1:
            next_x, next_y = solver_slice[1]
            next_center_x = (
                next_x * self.cell_size
                + self.outline_thickness
                + (self.cell_size - self.outline_thickness) // 2
            )
            next_center_y = (
                next_y * self.cell_size
                + self.outline_thickness
                + (self.cell_size - self.outline_thickness) // 2
            )

            thickness = self.outline_thickness + 1
            if center_x == next_center_x:
                y_start = min(center_y, next_center_y)
                length = abs(next_center_y - center_y) + thickness
                self.draw_line_v(
                    center_x - thickness // 2 + 1,
                    y_start - thickness // 2 + 1,
                    length,
                    color,
                    thickness,
                )
            else:
                x_start = min(center_x, next_center_x)
                length = abs(next_center_x - center_x) + thickness
                self.draw_line_h(
                    x_start - thickness // 2 + 1,
                    center_y - thickness // 2 + 1,
                    length,
                    color,
                    thickness,
                )

    def color_isoler(
        self,
        isoler: list[tuple[int, int]],
        cell_iso: tuple[int, int],
        color: int,
    ) -> None:
        iso_x, iso_y = cell_iso
        px = iso_x * self.cell_size + self.outline_thickness
        py = iso_y * self.cell_size + self.outline_thickness
        for x in range(px, px + self.cell_size - self.outline_thickness):
            for y in range(py, py + self.cell_size - self.outline_thickness):
                self.put_pixel(x, y, color)

        if (iso_x + 1, iso_y) in isoler:
            for dy in range(self.cell_size - self.outline_thickness):
                for t in range(self.outline_thickness + 1):
                    self.put_pixel(
                        px + self.cell_size - self.outline_thickness + t,
                        py + dy,
                        color,
                    )
        if (iso_x - 1, iso_y) in isoler:
            for dy in range(self.cell_size - self.outline_thickness):
                for t in range(self.outline_thickness + 1):
                    self.put_pixel(px - t, py + dy, color)
        if (iso_x, iso_y + 1) in isoler:
            for dx in range(self.cell_size - self.outline_thickness):
                for t in range(self.outline_thickness + 1):
                    self.put_pixel(
                        px + dx,
                        py + self.cell_size - self.outline_thickness + t,
                        color,
                    )
        if (iso_x, iso_y - 1) in isoler:
            for dx in range(self.cell_size - self.outline_thickness):
                for t in range(self.outline_thickness + 1):
                    self.put_pixel(px + dx, py - t, color)

    def clear_img(self) -> None:
        black = 0x1F000000
        for y in range(self.rows):
            for x in range(self.cols):
                self.put_pixel(x, y, black)

    def render_full(
        self, all_cell: list[Cell], isoler: list[tuple[int, int]], color: int
    ) -> None:
        for c in all_cell:
            if self.width >= 9 and self.height >= 8:
                if (c.x, c.y) not in isoler:
                    x0 = c.x * self.cell_size
                    y0 = c.y * self.cell_size

                    self.draw_line_h(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                    self.draw_line_v(
                        x0 + self.cell_size,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                    self.draw_line_h(
                        x0,
                        y0 + self.cell_size,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                    self.draw_line_v(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
            else:
                x0 = c.x * self.cell_size
                y0 = c.y * self.cell_size

                self.draw_line_h(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )
                self.draw_line_v(
                    x0 + self.cell_size,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )
                self.draw_line_h(
                    x0,
                    y0 + self.cell_size,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )
                self.draw_line_v(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self.img, 15, 15
        )

    def render(self, all_cell: list[Cell], color: int) -> None:
        the_width = (self.cols - self.outline_thickness) // self.cell_size
        the_height = (self.rows - self.outline_thickness) // self.cell_size
        isoler = isolated_cells(the_width, the_height)
        for c in all_cell:
            x0 = c.x * self.cell_size
            y0 = c.y * self.cell_size

            if self.width >= 9 and self.height >= 8:
                if (c.x, c.y) not in isoler:
                    if c.wall[0][0]:
                        self.draw_line_h(
                            x0,
                            y0,
                            self.cell_size + self.outline_thickness,
                            color,
                            self.outline_thickness,
                        )
                    if c.wall[1][0]:
                        self.draw_line_v(
                            x0 + self.cell_size,
                            y0,
                            self.cell_size + self.outline_thickness,
                            color,
                            self.outline_thickness,
                        )
                    if c.wall[2][0]:
                        self.draw_line_h(
                            x0,
                            y0 + self.cell_size,
                            self.cell_size + self.outline_thickness,
                            color,
                            self.outline_thickness,
                        )
                    if c.wall[3][0]:
                        self.draw_line_v(
                            x0,
                            y0,
                            self.cell_size + self.outline_thickness,
                            color,
                            self.outline_thickness,
                        )

            else:
                if c.wall[0][0]:
                    self.draw_line_h(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                if c.wall[1][0]:
                    self.draw_line_v(
                        x0 + self.cell_size,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                if c.wall[2][0]:
                    self.draw_line_h(
                        x0,
                        y0 + self.cell_size,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )
                if c.wall[3][0]:
                    self.draw_line_v(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        color,
                        self.outline_thickness,
                    )

    def draw_cell(
        self, cell: Cell, color: int, display_imp: bool = False
    ) -> None:
        x0 = cell.x * self.cell_size
        y0 = cell.y * self.cell_size

        if cell.wall[0][0] and cell.wall[0][1]:
            self.draw_line_h(
                x0,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        elif cell.wall[0][1]:
            self.delet_line_h(x0, y0, self.cell_size, self.outline_thickness)

        if cell.wall[1][0] and cell.wall[1][1]:
            self.draw_line_v(
                x0 + self.cell_size,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        elif cell.wall[1][1]:
            self.delet_line_v(
                x0 + self.cell_size,
                y0,
                self.cell_size,
                self.outline_thickness,
            )

        if cell.wall[2][0] and cell.wall[2][1]:
            self.draw_line_h(
                x0,
                y0 + self.cell_size,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        elif cell.wall[2][1]:
            self.delet_line_h(
                x0,
                y0 + self.cell_size,
                self.cell_size,
                self.outline_thickness,
            )

        if cell.wall[3][0] and cell.wall[3][1]:
            self.draw_line_v(
                x0,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        elif cell.wall[3][1]:
            self.delet_line_v(x0, y0, self.cell_size, self.outline_thickness)

        if display_imp:
            if not cell.wall[0][0] and not cell.wall[0][1]:
                self.draw_line_h(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )

            if not cell.wall[1][0] and not cell.wall[1][1]:
                self.draw_line_v(
                    x0 + self.cell_size,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )

            if not cell.wall[2][0] and not cell.wall[2][1]:
                self.draw_line_h(
                    x0,
                    y0 + self.cell_size,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )

            if not cell.wall[3][0] and not cell.wall[3][1]:
                self.draw_line_v(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    color,
                    self.outline_thickness,
                )

    def draw_cell_imperfect(
        self,
        cell: Cell,
        isoler: list[tuple[int, int]],
        color: int,
    ) -> None:
        x0 = cell.x * self.cell_size
        y0 = cell.y * self.cell_size

        if self.width >= 9 and self.height >= 8:
            if (cell.x, cell.y) not in isoler:
                if not cell.wall[0][0]:
                    self.delet_line_h(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        self.outline_thickness,
                        False,
                    )

                if not cell.wall[1][0]:
                    self.delet_line_v(
                        x0 + self.cell_size,
                        y0,
                        self.cell_size + self.outline_thickness,
                        self.outline_thickness,
                        False,
                    )

                if not cell.wall[2][0]:
                    self.delet_line_h(
                        x0,
                        y0 + self.cell_size,
                        self.cell_size + self.outline_thickness,
                        self.outline_thickness,
                        False,
                    )

                if not cell.wall[3][0]:
                    self.delet_line_v(
                        x0,
                        y0,
                        self.cell_size + self.outline_thickness,
                        self.outline_thickness,
                        False,
                    )
                self.draw_cell(cell, color)
        else:
            if not cell.wall[0][0]:
                self.delet_line_h(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    self.outline_thickness,
                    False,
                )

            if not cell.wall[1][0]:
                self.delet_line_v(
                    x0 + self.cell_size,
                    y0,
                    self.cell_size + self.outline_thickness,
                    self.outline_thickness,
                    False,
                )

            if not cell.wall[2][0]:
                self.delet_line_h(
                    x0,
                    y0 + self.cell_size,
                    self.cell_size + self.outline_thickness,
                    self.outline_thickness,
                    False,
                )

            if not cell.wall[3][0]:
                self.delet_line_v(
                    x0,
                    y0,
                    self.cell_size + self.outline_thickness,
                    self.outline_thickness,
                    False,
                )
            self.draw_cell(cell, color)

    def render_cell(self, a_cell: Cell, color: int) -> None:
        x0 = a_cell.x * self.cell_size
        y0 = a_cell.y * self.cell_size

        if a_cell.wall[0][0]:
            self.draw_line_h(
                x0,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        if a_cell.wall[1][0]:
            self.draw_line_v(
                x0 + self.cell_size,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        if a_cell.wall[2][0]:
            self.draw_line_h(
                x0,
                y0 + self.cell_size,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )
        if a_cell.wall[3][0]:
            self.draw_line_v(
                x0,
                y0,
                self.cell_size + self.outline_thickness,
                color,
                self.outline_thickness,
            )

    def fill_cell(
        self, all_stat: dict[str, Any], x: int, y: int, color: int
    ) -> None:
        px = x * self.cell_size
        py = y * self.cell_size
        for dx in range(self.outline_thickness, self.cell_size):
            for dy in range(self.outline_thickness, self.cell_size):
                self.put_pixel(px + dx, py + dy, color)

        a_cell = get_cell(all_stat["all_cell"], x, y, all_stat["WIDTH"])
        self.draw_cell_imperfect(
            a_cell, all_stat["isoler_original"], all_stat["color"][0]
        )

        if y - 1 >= 0 and (x, y - 1) not in self.isoler:
            a_cell = get_cell(
                all_stat["all_cell"], x, y - 1, all_stat["WIDTH"]
            )
            self.render_cell(a_cell, all_stat["color"][0])
        if x + 1 < all_stat["WIDTH"] and (x + 1, y) not in self.isoler:
            a_cell = get_cell(
                all_stat["all_cell"], x + 1, y, all_stat["WIDTH"]
            )
            self.render_cell(a_cell, all_stat["color"][0])
        if y + 1 < all_stat["HEIGHT"] and (x, y + 1) not in self.isoler:
            a_cell = get_cell(
                all_stat["all_cell"], x, y + 1, all_stat["WIDTH"]
            )
            self.render_cell(a_cell, all_stat["color"][0])
        if x - 1 >= 0 and (x - 1, y) not in self.isoler:
            a_cell = get_cell(
                all_stat["all_cell"], x - 1, y, all_stat["WIDTH"]
            )
            self.render_cell(a_cell, all_stat["color"][0])
