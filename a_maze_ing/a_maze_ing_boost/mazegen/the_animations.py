#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   the_animations.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 17:29:28 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/24 16:30:00 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .renderer import maze_mlx
from .generate_cellule.class_cell import Cell
from .generate_cellule.generate_cellule import get_cell
import random

# Importer les constantes
try:
    from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
except ImportError:
    CELL_SIZE = 20
    OUTLINE_THICKNESS = 2


def anime_solv(
    all_cell: list[Cell],
    the_window: maze_mlx,
    the_solv: list[tuple[int, int]],
    WIDTH: int,
    color: int,
) -> None:
    """Anime la résolution avec continuité des segments via last_pos."""
    
    # Mémoire persistante pour lier les paquets
    if not hasattr(anime_solv, "last_pos"):
        anime_solv.last_pos = None

    nbr = 5
    if len(the_solv) > 0:
        # 1. Raccordement : Relier le précédent lot au premier élément de celui-ci
        if anime_solv.last_pos is not None:
            prev = anime_solv.last_pos
            current = the_solv[0]
            the_window.color_content_solver(
                all_cell, WIDTH, prev[0], prev[1], 0, [prev, current], color
            )

        # 2. Dessiner le lot courant
        tmp = the_solv[:nbr]
        for i, (x, y) in enumerate(tmp):
            the_window.color_content_solver(
                all_cell, WIDTH, x, y, i, tmp, color
            )
            
        # 3. Mettre à jour la mémoire pour le prochain frame
        anime_solv.last_pos = tmp[-1]
        
        # 4. Consommer le lot
        del the_solv[:nbr]
    else:
        # On remet à zéro une fois terminé
        anime_solv.last_pos = None


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
            initial_color = 0xFF00FF00
            target_color = 0xFFFF0000

            a1 = (initial_color >> 24) & 0xFF
            r1 = (initial_color >> 16) & 0xFF
            g1 = (initial_color >> 8) & 0xFF
            b1 = initial_color & 0xFF

            a2 = (target_color >> 24) & 0xFF
            r2 = (target_color >> 16) & 0xFF
            g2 = (target_color >> 8) & 0xFF
            b2 = target_color & 0xFF

            progress = 1 - (len(solver) / solver_size) if solver_size > 0 else 1
            t = progress

            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            a = int(a1 + (a2 - a1) * t)

            color_solver = (a << 24) | (r << 16) | (g << 8) | b
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
        sms = "1: regen; 2: path; 3: color; 4: quit"
        the_window.mlx.mlx_string_put(
            the_window.mlx_ptr,
            the_window.win,
            COLS // 2 - (len(sms) * 5),
            ROWS + 35,
            0xFFFFFFFF,
            sms,
        )
