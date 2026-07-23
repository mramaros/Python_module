#!/usr/bin/env python3


from typing import Any
from .play_maze import play_the_maze
import sys
import os
import random


def start_maze(state: dict[str, Any]) -> None:
    """Fonction utilitaire pour lancer le labyrinthe."""
    state["my_window"].clear_img()
    state["start_screen"][0] = False
    state["tmp_sms"][0] = False

    try:
        state["my_window"].mlx.mlx_clear_window(
            state["my_window"].mlx_ptr, state["my_window"].win
        )
    except AttributeError:
        pass


def custom_handle_mouse(
    button: int, x: int, y: int, state: dict[str, Any]
) -> None:
    # la souri
    if state["tmp_sms"][0]:
        if state["start_screen"][0] and button == 1:
            x1, y1, x2, y2 = state["box_bounds"]
            box_x1, box_y1 = x1 + 15, y1 + 15
            box_x2, box_y2 = x2 + 15, y2 + 15

            if box_x1 <= x <= box_x2 and box_y1 <= y <= box_y2:
                start_maze(state)
    else:
        return


def custom_handle_keypress(keycode: int, state: dict[str, Any]) -> None:
    """
    Gestionnaire des événements clavier pour A-Maze-ing.
    Enter: Start ; 1: regen; 2: path; 3: color; 4: quit
    """
    w = state["my_window"]

    if keycode in (65307, 52, 65430):
        os._exit(0)

    if state["tmp_sms"][0]:
        if keycode in (65293, 65421) and state["start_screen"][0]:
            start_maze(state)
            return
    else:
        state["start_screen"][0] = False

    if state["start_screen"][0]:
        return

    if keycode in (49, 65436):
        for destroy_call, args in (
            ("mlx_destroy_image", (w.mlx_ptr, w.img)),
            ("mlx_destroy_window", (w.mlx_ptr, w.win)),
            ("mlx_destroy_display", (w.mlx_ptr,)),
        ):
            try:
                getattr(w.mlx, destroy_call)(*args)
            except AttributeError:
                pass
            except Exception:
                pass
        os.execv(sys.executable, [sys.executable] + sys.argv)
        return

    if keycode in (51, 65435):
        state["gamer_state"].play_or_not = False
        new_color = random.choice(state["list_color"])
        while new_color == state["color"][0]:
            new_color = random.choice(state["list_color"])
        old_color = state["color"][0]
        state["color"][0] = new_color

        if len(state["anime"]) > 0:
            w.put_pixel_all_image(old_color, new_color)
            w.mlx.mlx_put_image_to_window(w.mlx_ptr, w.win, w.img, 15, 15)
            return
        else:
            w.put_pixel_all_image(old_color, new_color)
            tmp_x, tmp_y = state["gamer_state"].pos
            state["ENTRY_X"][0] = tmp_x * w.cell_size + w.outline_thickness
            state["ENTRY_Y"][0] = tmp_y * w.cell_size + w.outline_thickness
            w.color_entry_and_exit(
                state["ENTRY_X"][0],
                state["ENTRY_Y"][0],
                state["EXIT_X"],
                state["EXIT_Y"],
            )

        if not state["isoler"]:
            new_color_iso = random.choice(state["list_color"])
            while new_color_iso == state["color_iso"]:
                new_color_iso = random.choice(state["list_color"])
            state["color_iso"] = new_color_iso

            for iso in state["isoler_original"]:
                w.color_isoler(
                    state["isoler_original"], iso, state["color_iso"]
                )

        return

    # --- DÉTECTION DES ANIMATIONS EN COURS ---
    is_animating = len(state["anime"]) > 0 or len(state["isoler"]) > 0
    if is_animating:
        return

    # --- Touche '2' (50, 19) : Path (Toggle Solveur On/Off) ---
    if keycode in (50, 65433):
        state["gamer_state"].play_or_not = False
        tmp_x, tmp_y = state["gamer_state"].pos
        state["ENTRY_X"][0] = tmp_x * w.cell_size + w.outline_thickness
        state["ENTRY_Y"][0] = tmp_y * w.cell_size + w.outline_thickness
        test = False
        if test:
            state["solver"][0] = state["class maze"].solver_dfs(
                state["ENTRY_X"][0],
                state["ENTRY_Y"][0],
                state["EXIT_X"],
                state["EXIT_Y"],
                w.outline_thickness,
                w.cell_size,
            )
        else:
            state["solver"][0] = state["class maze"].solver_bfs(
                state["ENTRY_X"][0],
                state["ENTRY_Y"][0],
                state["EXIT_X"],
                state["EXIT_Y"],
                w.outline_thickness,
                w.cell_size,
            )

        if not state["show_solver"][0]:
            state["show_solver"][0] = True

            if len(state["show_solver"]) == 1:
                state["show_solver"].append(0)
            else:
                state["show_solver"][1] = 0
        else:
            state["show_solver"][0] = False
            w.clear_img()
            w.render(state["all_cell"], state["color"][0])

            for iso in state["isoler_original"]:
                w.color_isoler(
                    state["isoler_original"], iso, state["color_iso"]
                )

            w.color_entry_and_exit(
                state["ENTRY_X"][0],
                state["ENTRY_Y"][0],
                state["EXIT_X"],
                state["EXIT_Y"],
            )
        return

    # --- Touche '5'
    if keycode in (53, 65437):
        state["gamer_state"].play_or_not = not state[
            "gamer_state"
        ].play_or_not

    # --- touche '6'
    if keycode in (54, 65432):
        if state["gamer_state"].pos != state["true_entry"]:
            state["show_solver"][0] = False
            w.clear_img()
            state["gamer_state"].play_or_not = False

            nx, ny = state["gamer_state"].exit_pos
            w.fill_cell(state, nx, ny, 0x11FF0000)

            state["gamer_state"].pos = state["true_entry"]
            tx, ty = state["true_entry"]
            w.fill_cell(state, tx, ty, 0x1100FF00)

            new_color = random.choice(state["list_color"])
            while new_color == state["color"][0]:
                new_color = random.choice(state["list_color"])
            state["color"][0] = new_color
            w.render(state["all_cell"], new_color)

            new_color_iso = random.choice(state["list_color"])
            while new_color_iso == state["color_iso"]:
                new_color_iso = random.choice(state["list_color"])
            state["color_iso"] = new_color_iso
            for iso in state["isoler_original"]:
                w.color_isoler(
                    state["isoler_original"], iso, state["color_iso"]
                )

    if state["gamer_state"].play_or_not:
        play_the_maze(
            keycode,
            state,
            state["class maze"],
            state["my_window"],
            state["all_cell"],
            state["isoler_original"],
            state["gamer_state"],
            state["true_entry"],
            state["gamer_state"].exit_pos,
            state["WIDTH"],
            state["HEIGHT"],
        )
        if (
            state["gamer_state"].pos == state["gamer_state"].exit_pos
            and not state["gamer_state"].play_or_not
        ):
            x, y = state["true_entry"]
            nx, ny = state["gamer_state"].exit_pos
            state["gamer_state"].pos = state["true_entry"]

            new_color = random.choice(state["list_color"])
            while new_color == state["color"][0]:
                new_color = random.choice(state["list_color"])
            state["color"][0] = new_color
            w.render(state["all_cell"], new_color)

            new_color_iso = random.choice(state["list_color"])
            while new_color_iso == state["color_iso"]:
                new_color_iso = random.choice(state["list_color"])
            state["color_iso"] = new_color_iso
            for iso in state["isoler_original"]:
                w.color_isoler(
                    state["isoler_original"], iso, state["color_iso"]
                )

            w.fill_cell(state, x, y, 0xFF00FF00)
            w.fill_cell(state, nx, ny, 0xFFFF0000)
        return
