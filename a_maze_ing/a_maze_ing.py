#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: raaron-v <raaron-v@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/15 13:29:11 by raaron-v            #+#    #+#            #
#   Updated: 2026/05/17 22:56:25 by raaron-v           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from mazegen import generated_maze, generated_maze_back
from mazegen import create_all_cells, get_cell
from mazegen import isolated_cells
from mazegen.generate_cellule import Cell


COLS = 0
ROWS = 0
CELL_SIZE = 20
OUTLINE_THICKNESS = 2


def read_config(the_file: str) -> list:
    """Lire le fichier de configuration et retourner les lignes (sans \n).

    Les lignes commentées (après '#') sont conservées ici mais le traitement
    ultérieur ignore la partie commentée.
    """
    config = []
    with open(the_file, 'r') as res:
        for line in res:
            config.append(line.rstrip("\n"))
    return config


def input_the_congif_maze(the_file: str) -> list:
    """Alias historique utilisé ailleurs — retourne les lignes du fichier de config."""
    return read_config(the_file)


def take_config(argv: str) -> dict:
    """Prendre les configurations à partir du fichier et les retourner dans un dictionnaire.

    Les lignes commentées (après '#') sont ignorées.
    Chaque ligne doit être au format "KEY=VALUE", sinon une exception est levée.
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

    for tmp in true_config:
        occurence = 0
        for ch in tmp:
            if ch == "=":
                occurence += 1

        if occurence != 1:
            raise SyntaxError(f"There is a small syntax error in your configuration file, here {tmp}")

    # Parse key/value pairs into the_dict
    for tmp in true_config:
        name, content = tmp.split("=", 1)
        the_dict[name] = content

    return the_dict




if __name__ == "__main__":
    try:

        if len(sys.argv) != 2:
            print(len(sys.argv))
            raise IndexError()
        config = input_the_congif_maze(sys.argv[1])

        print(config)

        true_config = []
        the_dict = {}
        for tmp in config:
            i = 0
            while i < len(tmp):
                if tmp[i] == "#":
                    break
                i += 1
            true_config.append(tmp[:i])

        print(true_config)

        for tmp in true_config:
            occurence = 0
            for ch in tmp:
                if ch == "=":
                    occurence += 1

            if occurence != 1:
                raise SyntaxError(f"There is a small syntax error in your configuration file, here {tmp}")

            name, content = tmp.split("=", 1)
            the_dict[name] = content

        name, content = tmp.split("=", 1)
        the_dict[name] = content

    except Exception as e:
        print("There is a small Error")
        print(e)

if __name__ == "__main__":
    try:
        the_dict = take_config(sys.argv[1])

        if "WIDTH" in the_dict and "HEIGHT" in the_dict:
            WIDTH = int(the_dict["WIDTH"])
            HEIGHT = int(the_dict["HEIGHT"])
            COLS = WIDTH * CELL_SIZE
            ROWS = HEIGHT * CELL_SIZE
        else:
            raise ValueError("The WIDTH or HEIGHT configurations do not exist.")

        all_cell = create_all_cells(WIDTH, HEIGHT)

        isolated = set()
        isolated: set = isolated_cells(WIDTH, HEIGHT)

        print("--- BEFORE ---\n")
        i = 0 # index for iterating through all_cell
        jump = 0 # counter to track when to print a newline
        while i < len(all_cell):
            all_cell[i].draw()
            jump += 1
            if jump >= WIDTH:
                print()
                jump = 0
            i += 1
        # print(len(all_cell))

        generated_maze(all_cell, isolated, WIDTH, HEIGHT)

        print("\n--- AFTER ---")
        # build lines for AFTER and write to output file if provided
        after_lines = []
        for y in range(HEIGHT):
            line = ""
            for x in range(WIDTH):
                line += get_cell(all_cell, x, y, WIDTH).hex_char()
            after_lines.append(line)
            print(line)

        try:
            '''
            La, il ecrit le resultat dans un fichier de sortie "output_maze.txt".
            Si une exception se produit lors de l'écriture du fichier, elle est ignorée.
            '''
            with open("output_maze.txt", "w") as out:
                for l in after_lines:
                    out.write(l + "\n")
        except Exception:
            pass

        # Try to open an MLX window showing the maze (optional)
        try:
            from mazegen.renderer import MazeRenderer

            maze_mat = []
            for y in range(HEIGHT):
                row = []
                for x in range(WIDTH):
                    c = get_cell(all_cell, x, y, WIDTH)
                    val = c.wall[3] * 8 + c.wall[2] * 4 + c.wall[1] * 2 + c.wall[0] * 1
                    row.append(val)
                maze_mat.append(row)

            def _regen():
                new_cells = create_all_cells(WIDTH, HEIGHT)
                new_iso = isolated_cells(WIDTH, HEIGHT)
                generated_maze(new_cells, new_iso, WIDTH, HEIGHT)
                new_mat = []
                for _y in range(HEIGHT):
                    _row = []
                    for _x in range(WIDTH):
                        _c = get_cell(new_cells, _x, _y, WIDTH)
                        _row.append(_c.wall[3]*8 + _c.wall[2]*4 + _c.wall[1]*2 + _c.wall[0]*1)
                    new_mat.append(_row)
                return new_mat

            renderer = MazeRenderer(maze_mat, WIDTH, HEIGHT, isolated)
            renderer.set_regen_callback(_regen)
            renderer.run()
        except Exception as e:
            print("MLX renderer not started:", e)

    except IndexError:
        print("There is a small Error")
        print("Verify that you are launching the program correctly as follows: ", end="")
        print("python3 a_maze_ing.py config.txt")
    except SyntaxError as e:
        print("There is a small Error")
        print(e)