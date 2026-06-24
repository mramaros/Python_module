#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   the_animations.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/11 17:29:28 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/23 12:00:00 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from .renderer import maze_mlx
from .generate_cellule.class_cell import Cell
from .generate_cellule.generate_cellule import get_cell
import random

# Importer les constantes depuis a_maze_ing.py
try:
    from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
except ImportError:
    # Valeurs par défaut si l'import échoue
    CELL_SIZE = 20
    OUTLINE_THICKNESS = 2


def anime_solv(
    all_cell: list[Cell],
    the_window: maze_mlx,
    the_solv: list[tuple[int, int]],
    WIDTH: int,
    color: int,
) -> None:
    """
    Anime la résolution du labyrinthe en affichant le chemin progressivement.
    
    Paramètres:
    - all_cell: liste de toutes les cellules
    - the_window: fenêtre MLX
    - the_solv: liste des coordonnées du chemin à afficher
    - WIDTH: largeur du labyrinthe en cellules
    - color: couleur du chemin
    """
    nbr = 5
    if len(the_solv) > 0:
        tmp = the_solv[:nbr]
        the_solv[:] = the_solv[nbr:]

        for i, (x, y) in enumerate(tmp):
            the_window.color_content_solver(
                all_cell, WIDTH, x, y, i, tmp, color
            )


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
    """
    Fonction principale d'animation appelée par la boucle MLX.
    
    Gère 3 phases :
    1. Génération du labyrinthe (affichage progressif des cellules)
    2. Colorisation des cellules isolées (motif "42")
    3. Résolution du labyrinthe (affichage du chemin)
    
    Paramètres:
    - the_anime: liste des cellules à afficher pendant la génération
    - solver: liste des coordonnées du chemin résolu
    - solver_size: taille totale du chemin
    - the_window: fenêtre MLX
    - all_cell: liste de toutes les cellules
    - isoler: liste des cellules isolées (motif "42")
    - color: couleur des murs
    - color_iso: couleur des cellules isolées
    - list_color: liste de couleurs disponibles
    - WIDTH, HEIGHT: dimensions du labyrinthe en cellules
    - ENTRY_X, ENTRY_Y: coordonnées de l'entrée en pixels
    - EXIT_X, EXIT_Y: coordonnées de la sortie en pixels
    - COLS, ROWS: dimensions de la fenêtre en pixels
    - already_printed: flag pour afficher les instructions une seule fois
    """
    nbr = 5
    
    # ===== PHASE 1 : Génération du labyrinthe =====
    if len(the_anime) > 0:
        WHAO = the_anime[:nbr]
        the_anime[:] = the_anime[nbr:]
        for x, y in WHAO:
            # 🔥 Utiliser les TEXTURES au lieu des couleurs
            the_window.draw_cell_with_texture(
                get_cell(all_cell, x, y, WIDTH),
                WIDTH,
                HEIGHT,
                CELL_SIZE,
                OUTLINE_THICKNESS,
                all_cell
            )
    
    # ===== PHASE 2 : Colorisation des cellules isolées =====
    elif len(isoler) > 0:
        a_iso = isoler.pop(0)
        the_window.color_isoler(isoler, a_iso, color_iso)
        the_window.color_entry_and_exit(ENTRY_X, ENTRY_Y, EXIT_X, EXIT_Y)

    # ===== PHASE 3 : Résolution du labyrinthe =====
    else:
        # Dégradé de couleur du vert vers le rouge
        initial_color = 0xFF00FF00  # Vert
        target_color = 0xFFFF0000   # Rouge

        a1 = (initial_color >> 24) & 0xFF
        r1 = (initial_color >> 16) & 0xFF
        g1 = (initial_color >> 8) & 0xFF
        b1 = initial_color & 0xFF

        a2 = (target_color >> 24) & 0xFF
        r2 = (target_color >> 16) & 0xFF
        g2 = (target_color >> 8) & 0xFF
        b2 = target_color & 0xFF

        progress = 1 - (len(solver) / solver_size)
        t = progress  # 0 → 1

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        a = int(a1 + (a2 - a1) * t)

        color_solver = (a << 24) | (r << 16) | (g << 8) | b
        anime_solv(all_cell, the_window, solver, WIDTH, color_solver)

    # Mettre à jour l'affichage
    the_window.mlx.mlx_put_image_to_window(
        the_window.mlx_ptr, the_window.win, the_window.img, 15, 15
    )

    # Afficher les instructions une seule fois
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
