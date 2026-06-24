#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/15 13:29:11 by raaron-v            #+#    #+#            #
#   Updated: 2026/06/16 08:31:49 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from mazegen import generated_maze_back
from mazegen import create_all_cells, get_cell
from mazegen import isolated_cells
from mazegen import solver_back
import random

CELL_SIZE = 42
OUTLINE_THICKNESS = 7


def read_config(the_file: str) -> list:
    """
    Lire le fichier de configuration et retourner les lignes (sans \n).
    Les lignes commentées (après '#') sont conservées ici mais le traitement
    ultérieur ignore la partie commentée.
    """
    config = []
    with open(the_file, "r") as res:
        for line in res:
            config.append(line.rstrip("\n"))
    return config


def input_the_congif_maze(the_file: str) -> list:
    """
    Alias historique utilisé ailleurs —
    retourne les lignes du fichier de config.
    """

    return read_config(the_file)


def take_config(argv: str) -> dict:
    """
    Prendre les configurations à partir du fichier
    et les retourner dans un dictionnaire.

    Les lignes commentées (après '#') sont ignorées.
    Chaque ligne doit être au format "KEY=VALUE",
    sinon une exception est levée.
    """
    config = read_config(argv)
    true_config = []
    the_dict = {}
    for tmp in config:
        i = 0
        while i < len(tmp):
            if tmp[i] == "#":
                break
            i += 1
        true_config.append(tmp[:i])

    # enleve les chaine vide
    only_not_vide = []
    for ch in true_config:
        if len(ch) != 0:
            only_not_vide.append(ch)

    true_config = only_not_vide
    for tmp in true_config:
        occurence = 0
        for ch in tmp:
            if ch == "=":
                occurence += 1

        if occurence != 1:
            raise SyntaxError(
                "There is a small syntax error in your configuration file, "
                f"here {tmp}"
            )

    # Parse key/value pairs into the_dict
    for tmp in true_config:
        name, content = tmp.split("=", 1)
        the_dict[name] = content

    # verifie si ils sont bien synatax
    for one, two in the_dict.items():
        if len(one) == 0 or len(two) == 0:
            raise SyntaxError(
                f"that syntax key = '{one}' or/and value = '{two}'"
                " is incorrect."
            )

    return the_dict


if __name__ == "__main__":
    try:
        COLS = 0
        ROWS = 0
        list_color = [
            0xFF00FFFF,
            0xFFFFFF00,
            0xFF0000FF,
            0xFF87CEEB,
            0xFFFFA500,
        ]
        color = random.choice(list_color)
        color_iso = random.choice(list_color)

        the_dict = take_config(sys.argv[1])

        if "WIDTH" in the_dict and "HEIGHT" in the_dict:
            WIDTH = int(the_dict["WIDTH"])
            HEIGHT = int(the_dict["HEIGHT"])
            COLS = WIDTH * CELL_SIZE + OUTLINE_THICKNESS
            ROWS = HEIGHT * CELL_SIZE + OUTLINE_THICKNESS
        else:
            raise ValueError(
                "The WIDTH or HEIGHT configurations do not exist."
            )

        if "ENTRY" in the_dict and "EXIT" in the_dict:
            tmp_x, tmp_y = the_dict["ENTRY"].split(",", 1)
            ENTRY_X = int(tmp_x) * CELL_SIZE + OUTLINE_THICKNESS
            ENTRY_Y = int(tmp_y) * CELL_SIZE + OUTLINE_THICKNESS

            tmp_x, tmp_y = the_dict["EXIT"].split(",", 1)
            EXIT_X = int(tmp_x) * CELL_SIZE + OUTLINE_THICKNESS
            EXIT_Y = int(tmp_y) * CELL_SIZE + OUTLINE_THICKNESS
        else:
            raise ValueError(
                "The ENTRY or EXIT configurations do not exist."
            )

        all_cell = create_all_cells(WIDTH, HEIGHT)

        isolated = set()
        isolated: set(list[str, ]) = isolated_cells(WIDTH, HEIGHT)

        save_for_anime = generated_maze_back(
            all_cell, isolated, WIDTH, HEIGHT
        )
        solver = solver_back(
            all_cell,
            WIDTH,
            ENTRY_X,
            ENTRY_Y,
            EXIT_X,
            EXIT_Y,
            OUTLINE_THICKNESS,
            CELL_SIZE,
        )
        solver_size = len(solver)
        after_lines = []
        for y in range(HEIGHT):
            line = ""
            for x in range(WIDTH):
                line += get_cell(all_cell, x, y, WIDTH).hex_char()
            after_lines.append(line)

        try:
            """
            La, il ecrit le resultat dans un fichier de sortie "output_maze.txt".
            Si une exception se produit lors de l'écriture du fichier, elle est ignorée.
            """
            with open("output_maze.txt", "w") as out:
                for string in after_lines:
                    out.write(string + "\n")
        except Exception:
            pass

        # Try to open an MLX window showing the maze (optional)

        # Try to open an MLX window showing the maze (optional)
        try:
            from mazegen import maze_mlx, anime

            my_window = maze_mlx(COLS, ROWS, CELL_SIZE, OUTLINE_THICKNESS)
            
            # --- NOUVEAU : Rendu avec textures ---
            # Appeler render_with_textures pour dessiner le labyrinthe avec les images
            my_window.render_with_textures(
                all_cell,
                WIDTH,
                HEIGHT,
                CELL_SIZE,
                OUTLINE_THICKNESS
            )
            # --- FIN NOUVEAU ---
            
            already_printed = [False]
            my_window.mlx.mlx_loop_hook(
                my_window.mlx_ptr,
                lambda d: anime(
                    save_for_anime,
                    solver,
                    solver_size,
                    my_window,
                    all_cell,
                    isolated,
                    color,
                    color_iso,
                    list_color,
                    WIDTH,
                    HEIGHT,
                    ENTRY_X,
                    ENTRY_Y,
                    EXIT_X,
                    EXIT_Y,
                    COLS,
                    ROWS,
                    already_printed,
                ),
                None,
            )

            my_window.mlx.mlx_hook(
                my_window.win,
                33,
                0,
                lambda e: my_window.mlx.mlx_loop_exit(my_window.mlx_ptr),
                None,
            )
            my_window.mlx.mlx_loop(my_window.mlx_ptr)
        except Exception as e:
            print(f"MLX renderer not started: {e}")

    except IndexError:
        print("There is a small Error")
        print("Verify that you are launching the program correctly", end="")
        print(" as follows: ", end="")

        print("make")
        print("make run")
    except SyntaxError as e:
        print("There is a small Error")
        print(e)
