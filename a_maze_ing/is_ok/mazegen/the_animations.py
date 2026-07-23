#!/usr/bin/env python3

from .renderer import MazeMlx
from .generate_cellule.class_cell import Cell
from .classe_maze_generator import MazeGenerator


def anime_solv(
    all_cell: list[Cell],
    the_window: MazeMlx,
    the_solv: list[tuple[int, int]],
    color: int,
    show_solver: list[int],
) -> None:

    nbr = 3
    if len(show_solver) < 2:
        show_solver.append(0)

    start_idx = show_solver[1]
    end_idx = min(start_idx + nbr, len(the_solv) - 1)

    for i in range(start_idx, end_idx):
        x, y = the_solv[i]
        slice_solv = the_solv[i: i + 2]
        the_window.color_content_solver(all_cell, x, y, slice_solv, color)

    if start_idx < len(the_solv) - 1:
        show_solver[1] = end_idx


def anime(
    display: list[bool],
    display_sms: list[bool],
    class_maze: MazeGenerator,
    the_maze: list[tuple[int, int]],
    solver: list[tuple[int, int]],
    solver_size: int,
    the_window: MazeMlx,
    all_cell: list[Cell],
    tmp_all_cell: list[Cell],
    perfect: list[bool],
    isoler: list[tuple[int, int]],
    color_ref: list[int],
    color_iso: int,
    list_color: list[int],
    width: int,
    height: int,
    entry_x_px: int,
    entry_y_px: int,
    exit_x_px: int,
    exit_y_px: int,
    cols: int,
    rows: int,
    already_printed: list[bool],
    only_once: list[bool],
    show_solver: list[int],
    start_screen: list[bool],
    box_bounds: list[int],
    start_printed: list[bool],
    animate_gen: bool,
    speed: int,
) -> None:

    # GESTION DE L'ÉCRAN D'ACCUEIL
    if start_screen[0] and display_sms[0]:
        if not start_printed[0]:
            the_window.clear_img()

            title_str = "A - MAZE - ING"
            push_str = "CLICK OR ENTER TO START"

            char_w = 6
            char_h = 10

            title_w = len(title_str) * char_w
            push_w = len(push_str) * char_w
            content_w = max(title_w, push_w)

            pad_x = 45
            pad_y = 25
            line_gap = 20

            box_w = content_w + pad_x * 4
            box_h = pad_y * 2 + char_h * 2 + line_gap

            cx = cols // 2
            cy = rows // 2
            x1 = cx - box_w // 2
            y1 = cy - box_h // 2
            x2 = cx + box_w // 2
            y2 = cy + box_h // 2

            box_bounds[0], box_bounds[1], box_bounds[2], box_bounds[3] = (
                x1,
                y1,
                x2,
                y2,
            )

            color_white = 0xFFFFFFFF
            thickness = 2
            the_window.draw_line_h(x1, y1, box_w, color_white, thickness)
            the_window.draw_line_h(x1, y2, box_w, color_white, thickness)
            the_window.draw_line_v(x1, y1, box_h, color_white, thickness)
            the_window.draw_line_v(
                x2, y1, box_h + thickness, color_white, thickness
            )

            the_window.mlx.mlx_put_image_to_window(
                the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
            )

            title_y = y1 + pad_y
            push_y = title_y + char_h + line_gap

            the_window.mlx.mlx_string_put(
                the_window.mlx_ptr,
                the_window.win,
                cx - (len(title_str) * 3) - 20,
                title_y + 15,
                color_white,
                title_str,
            )

            the_window.mlx.mlx_string_put(
                the_window.mlx_ptr,
                the_window.win,
                cx - (len(push_str) * 3) - 20,
                push_y + 15,
                color_white,
                push_str,
            )
            start_printed[0] = True
        return

    color = color_ref[0]

    # --- MODIFICATION DE LA LOGIQUE DE DESSIN ---
    if display[0]:
        the_window.render_full(
            all_cell, isoler, color
        )
        display[0] = False

    if len(the_maze) > 0:
        nbr = max(4, speed) if animate_gen else len(the_maze)
        tmp = the_maze[:nbr]
        the_maze[:] = the_maze[nbr:]
        for x, y in tmp:
            cell = class_maze.get_cell(x, y)
            the_window.draw_cell(cell, color, True)

    elif len(tmp_all_cell) > 0 and not perfect[0]:
        nbr = max(1, width // 4) if animate_gen else len(tmp_all_cell)
        cell_chunk = tmp_all_cell[:nbr]
        tmp_all_cell[:] = tmp_all_cell[nbr:]
        for a_cell in cell_chunk:
            the_window.draw_cell_imperfect(a_cell, isoler, color)

    elif not only_once[0]:
        only_once[0] = True
        the_window.render(all_cell, color)
        the_window.color_entry_and_exit(
            entry_x_px, entry_y_px, exit_x_px, exit_y_px
        )

    else:
        if len(isoler) > 0:
            if width >= 9 and height >= 8:
                nbr = 2 if animate_gen else len(isoler)
                for _ in range(nbr):
                    a_iso = isoler.pop(0)
                    the_window.color_isoler(isoler, a_iso, color_iso)

        else:
            # Animation du solveur (on la laisse telle quelle pour le style)
            if show_solver[0]:
                initial_color = 0x1100FF00
                target_color = 0x11FF0000

                a1 = (initial_color >> 24) & 0xFF
                r1 = (initial_color >> 16) & 0xFF
                g1 = (initial_color >> 8) & 0xFF
                b1 = initial_color & 0xFF

                a2 = (target_color >> 24) & 0xFF
                r2 = (target_color >> 16) & 0xFF
                g2 = (target_color >> 8) & 0xFF
                b2 = target_color & 0xFF

                current_idx = show_solver[1] if len(show_solver) > 1 else 0
                progress = current_idx / solver_size if solver_size > 0 else 1
                t = progress

                r = int(r1 + (r2 - r1) * t)
                g = int(g1 + (g2 - g1) * t)
                b = int(b1 + (b2 - b1) * t)
                a = int(a1 + (a2 - a1) * t)

                color_iso_calc = (a << 24) | (r << 16) | (g << 8) | b
                anime_solv(
                    all_cell, the_window, solver, color_iso_calc, show_solver
                )

    the_window.mlx.mlx_put_image_to_window(
        the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
    )

    if not already_printed[0]:
        already_printed[0] = True
        sms = "1: Regen; 2: Path; 3: Color; 4: Quit; 5:Play; 6: Start Over;"
        the_window.mlx.mlx_string_put(
            the_window.mlx_ptr,
            the_window.win,
            cols // 2 - (len(sms) * 5),
            rows + 30,
            0x1FFFFFFF,
            sms,
        )
