#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   the_animations.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 17:29:28 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/25 13:40:00 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .renderer import maze_mlx
from .generate_cellule.class_cell import Cell
from .generate_cellule.generate_cellule import get_cell

try:
    from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
except ImportError:
    CELL_SIZE = 26
    OUTLINE_THICKNESS = max(1, int(CELL_SIZE * 0.4375))


# --------------------------------------------------------------------------- #
#   anime_solv — tracé continu du chemin de résolution                        #
# --------------------------------------------------------------------------- #

def anime_solv(
    all_cell: list[Cell],
    the_window: maze_mlx,
    the_solv: list[tuple[int, int]],
    WIDTH: int,
    color: int,
) -> None:
    """Anime la résolution avec anticipation pour lier les segments."""
    nbr = 5
    if len(the_solv) > 0:
        tmp_lookahead = the_solv[:nbr + 1]
        tmp = the_solv[:nbr]
        the_solv[:] = the_solv[nbr:]
        for i, (x, y) in enumerate(tmp):
            the_window.color_content_solver(
                all_cell, WIDTH, x, y, i, tmp_lookahead, color
            )


# --------------------------------------------------------------------------- #
#   _lerp_color — interpolation linéaire entre deux couleurs ARGB             #
# --------------------------------------------------------------------------- #

def _lerp_color(c1: int, c2: int, t: float) -> int:
    a1, r1, g1, b1 = (c1 >> 24) & 0xFF, (c1 >> 16) & 0xFF, (c1 >> 8) & 0xFF, c1 & 0xFF
    a2, r2, g2, b2 = (c2 >> 24) & 0xFF, (c2 >> 16) & 0xFF, (c2 >> 8) & 0xFF, c2 & 0xFF
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    a = int(a1 + (a2 - a1) * t)
    return (a << 24) | (r << 16) | (g << 8) | b


# --------------------------------------------------------------------------- #
#   loop_erase — un frame d'effacement rétractif du solveur                   #
# --------------------------------------------------------------------------- #

def loop_erase(state: dict) -> None:
    """Appelée chaque frame quand solver_state == 'erasing'."""
    state["erase_index"] -= 3
    if state["erase_index"] < 0:
        state["erase_index"] = 0

    win = state["my_window"]

    # Restauration ultra-rapide depuis le cache mémoire
    if "clean_bg_data" in state:
        win.data[:] = state["clean_bg_data"]

    if state["erase_index"] > 0:
        partial = state["backup_solver"][:state["erase_index"]]
        progress = 1 - (len(partial) / state["solver_size"]) if state["solver_size"] > 0 else 1
        color_solver = _lerp_color(state["color"], 0xFF2F4F4F, progress)

        for i, (x, y) in enumerate(partial):
            if i >= len(partial) - 3:
                glow = 0xFFFFFFFF if i == len(partial) - 1 else 0xFFFFA500
                win.color_content_solver(state["all_cell"], state["WIDTH"], x, y, i, partial, glow)
            else:
                win.color_content_solver(state["all_cell"], state["WIDTH"], x, y, i, partial, color_solver)

        # Traînée de braises sur les cellules fraîchement effacées
        just_erased = state["backup_solver"][state["erase_index"]:state["erase_index"] + 12]
        for idx, (x, y) in enumerate(just_erased):
            t_glow = idx / 12
            r_g = int(255 * (1 - t_glow))
            g_g = max(0, int(120 * (1 - t_glow * 1.5)))
            a_g = int(255 * (1 - t_glow))
            spark = (a_g << 24) | (r_g << 16) | (g_g << 8) | 0
            win.color_content_solver(
                state["all_cell"], state["WIDTH"],
                x, y,
                state["erase_index"] + idx,
                state["backup_solver"],
                spark,
            )
    else:
        state["solver_state"] = "hidden"
        print("⏹️ Solveur complètement effacé.")

    win.mlx.mlx_put_image_to_window(win.mlx_ptr, win.win, win.img, 15, 15)


# --------------------------------------------------------------------------- #
#   loop_wrapper — hook principal appelé à chaque frame par MLX               #
# --------------------------------------------------------------------------- #

def loop_wrapper(state: dict, _d=None) -> None:
    """
    Enveloppe la boucle MLX.
    Gère les transitions : drawing → shown, et delègue à loop_erase ou anime.
    """
    # Transition drawing → shown
    if state["solver_state"] == "drawing" and len(state["solver"]) == 0:
        state["solver_state"] = "shown"
        print("🏁 Solveur entièrement affiché.")

    # Phase effacement
    if state["solver_state"] == "erasing":
        loop_erase(state)
        return

    # Capture du background une fois la grille + "42" affichés
    if (
        len(state["anime"]) == 0
        and len(state["isoler"]) == 0
        and "clean_bg_data" not in state
    ):
        state["clean_bg_data"] = bytes(state["my_window"].data)
        print("📸 Cache mémoire du labyrinthe mis à jour (Prêt pour le solveur) !")

    # Comportement standard
    anime(
        state["anime"],
        state["solver"],
        state["solver_size"],
        state["my_window"],
        state["all_cell"],
        state["isoler"],
        state["color"],
        state["color_iso"],
        state["list_color"],
        state["WIDTH"],
        state["HEIGHT"],
        state["ENTRY_X"],
        state["ENTRY_Y"],
        state["EXIT_X"],
        state["EXIT_Y"],
        state["COLS"],
        state["ROWS"],
        state["already_printed"],
    )


# --------------------------------------------------------------------------- #
#   anime — animation frame-by-frame (génération → motif 42 → résolution)    #
# --------------------------------------------------------------------------- #

def anime(
    the_anime: list[tuple[int, int]],
    solver: list[tuple[int, int]],
    solver_size: int,
    the_window: maze_mlx,
    all_cell: list[Cell],
    isoler: list[tuple[int, int]],
    color: int,
    color_iso: int,
    list_color: list[int],
    WIDTH: int,
    HEIGHT: int,
    ENTRY_X: int,
    ENTRY_Y: int,
    EXIT_X: int,
    EXIT_Y: int,
    COLS: int,
    ROWS: int,
    already_printed: list[bool],
) -> None:
    """Fonction principale d'animation appelée par la boucle MLX."""
    nbr = 5

    # ===== PHASE 1 : Génération du labyrinthe =====
    if len(the_anime) > 0:
        if getattr(the_window, "_needs_clear", True) or len(the_anime) == WIDTH * HEIGHT:
            the_window.clear_img()
            if hasattr(the_window, "fill_all_ground"):
                the_window.fill_all_ground(WIDTH, HEIGHT)
            the_window._needs_clear = False

        WHAO = the_anime[:nbr]
        the_anime[:] = the_anime[nbr:]
        for x, y in WHAO:
            the_window.draw_cell_with_texture(
                get_cell(all_cell, x, y, WIDTH),
                WIDTH, HEIGHT, CELL_SIZE, OUTLINE_THICKNESS, all_cell
            )
        the_window.mlx.mlx_put_image_to_window(
            the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
        )

    # ===== PHASE 2 : Colorisation Motif 42 =====
    elif len(isoler) > 0:
        if not hasattr(the_window, "all_isolated_set"):
            the_window.all_isolated_set = set(isoler)

        tmp_iso = isoler[:nbr]
        isoler[:] = isoler[nbr:]
        for a_iso in tmp_iso:
            the_window.color_isoler(the_window.all_isolated_set, a_iso, color_iso)

        the_window.color_entry_and_exit(ENTRY_X, ENTRY_Y, EXIT_X, EXIT_Y)
        the_window.mlx.mlx_put_image_to_window(
            the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
        )

    # ===== PHASE 3 : Résolution =====
    else:
        if len(solver) > 0:
            progress = 1 - (len(solver) / solver_size) if solver_size > 0 else 1
            color_solver = _lerp_color(color, 0xFFFF0000, progress)
            anime_solv(all_cell, the_window, solver, WIDTH, color_solver)
        else:
            the_window._needs_clear = True
            if hasattr(the_window, "all_isolated_set"):
                del the_window.all_isolated_set

        the_window.mlx.mlx_put_image_to_window(
            the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
        )

    if not already_printed[0]:
        already_printed[0] = True
        sms = "1: regen; 2: path; 3: color/biome; 4: quit"
        the_window.mlx.mlx_string_put(
            the_window.mlx_ptr,
            the_window.win,
            COLS // 2 - (len(sms) * 5),
            ROWS + 35,
            0xFFFFFFFF,
            sms,
        )
