#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/15 13:29:11 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/25 17:15:00 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
import random

from mazegen import create_all_cells, get_cell, isolated_cells
from mazegen import generated_maze_back, solver_back
from mazegen.config import take_config

CELL_SIZE          = 36
OUTLINE_THICKNESS  = max(1, int(CELL_SIZE * 0.4375))


if __name__ == "__main__":
    try:
        list_color = [0xFF00FFFF, 0xFFFFFF00, 0xFF0000FF, 0xFF87CEEB, 0xFFFFA500]
        color     = random.choice(list_color)
        color_iso = random.choice(list_color)

        the_dict = take_config(sys.argv[1])

        if "WIDTH" not in the_dict or "HEIGHT" not in the_dict:
            raise ValueError("The WIDTH or HEIGHT configurations do not exist.")
        WIDTH  = int(the_dict["WIDTH"])
        HEIGHT = int(the_dict["HEIGHT"])
        COLS   = WIDTH  * CELL_SIZE + OUTLINE_THICKNESS
        ROWS   = HEIGHT * CELL_SIZE + OUTLINE_THICKNESS

        if "ENTRY" not in the_dict or "EXIT" not in the_dict:
            raise ValueError("The ENTRY or EXIT configurations do not exist.")
        ex, ey   = the_dict["ENTRY"].split(",", 1)
        ENTRY_X  = int(ex) * CELL_SIZE + OUTLINE_THICKNESS
        ENTRY_Y  = int(ey) * CELL_SIZE + OUTLINE_THICKNESS
        xx, xy   = the_dict["EXIT"].split(",", 1)
        EXIT_X   = int(xx) * CELL_SIZE + OUTLINE_THICKNESS
        EXIT_Y   = int(xy) * CELL_SIZE + OUTLINE_THICKNESS

        all_cell    = create_all_cells(WIDTH, HEIGHT)
        isolated    = isolated_cells(WIDTH, HEIGHT)
        save_anime  = generated_maze_back(all_cell, isolated, WIDTH, HEIGHT)
        solver      = solver_back(all_cell, WIDTH, ENTRY_X, ENTRY_Y, EXIT_X, EXIT_Y,
                                  OUTLINE_THICKNESS, CELL_SIZE)
        solver_size = len(solver)

        # Écriture du labyrinthe en hexadécimal
        try:
            with open("output_maze.txt", "w") as out:
                for y in range(HEIGHT):
                    out.write(
                        "".join(get_cell(all_cell, x, y, WIDTH).hex_char() for x in range(WIDTH))
                        + "\n"
                    )
        except Exception:
            pass

        # ── Rendu graphique ──────────────────────────────────────────────── #
        try:
            from mazegen import maze_mlx
            from mazegen.the_animations import loop_wrapper
            from mazegen.key_maps import custom_handle_keypress

            my_window = maze_mlx(COLS, ROWS, CELL_SIZE, OUTLINE_THICKNESS)

            state = {
                "my_window":      my_window,
                "all_cell":       all_cell,
                "WIDTH":          WIDTH,
                "HEIGHT":         HEIGHT,
                "COLS":           COLS,
                "ROWS":           ROWS,
                "CELL_SIZE":      CELL_SIZE,
                "OUTLINE_THICKNESS": OUTLINE_THICKNESS,
                "ENTRY_X":        ENTRY_X,
                "ENTRY_Y":        ENTRY_Y,
                "EXIT_X":         EXIT_X,
                "EXIT_Y":         EXIT_Y,
                "color":          color,
                "color_iso":      color_iso,
                "list_color":     list_color,
                "anime":          list(save_anime),
                "backup_anime":   list(save_anime),
                "isoler":         list(isolated),
                "backup_isoler":  list(isolated),
                "solver":         [],
                "backup_solver":  list(solver),
                "solver_size":    solver_size,
                "solver_state":   "hidden",
                "erase_index":    0,
                "env_idx":        0,
                "already_printed": [False],
            }

            my_window.mlx.mlx_loop_hook(
                my_window.mlx_ptr,
                lambda d: loop_wrapper(state, d),
                None,
            )
            my_window.mlx.mlx_hook(
                my_window.win, 2, 1,
                lambda keycode, d: custom_handle_keypress(keycode, state),
                None,
            )
            my_window.mlx.mlx_hook(
                my_window.win, 33, 0,
                lambda e: my_window.mlx.mlx_loop_exit(my_window.mlx_ptr),
                None,
            )
            my_window.mlx.mlx_loop(my_window.mlx_ptr)

        except Exception as e:
            print(f"MLX renderer not started: {e}")

    except IndexError:
        print("There is a small Error\nVerify execution: make\nmake run")
    except (SyntaxError, ValueError) as e:
        print(f"There is a small Error\n{e}")
