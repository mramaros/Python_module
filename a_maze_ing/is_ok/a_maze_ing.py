#!/usr/bin/env python3


import sys
from typing import Any
from mazegen import MazeGenerator, GameState
from mazegen import solver_in_nesw
import random

title = [
    "    █████╗           ███╗   ███╗  █████╗ ███████╗███████╗          "
    "██╗███╗   ██╗ ██████╗",
    "   ██╔══██╗          ████╗ ████║ ██╔══██╗╚══███╔╝██╔════╝          "
    "██║████╗  ██║██╔════╝",
    "   ███████║  █████╗  ██╔████╔██║ ███████║  ███╔╝ █████╗    █████╗  "
    "██║██╔██╗ ██║██║  ███╗",
    "   ██╔══██║  ╚════╝  ██║╚██╔╝██║ ██╔══██║ ███╔╝  ██╔══╝    ╚════╝  "
    "██║██║╚██╗██║██║   ██║",
    "   ██║  ██║          ██║ ╚═╝ ██║ ██║  ██║███████╗███████╗          "
    "██║██║ ╚████║╚██████╔╝",
    "   ╚═╝  ╚═╝          ╚═╝     ╚═╝ ╚═╝  ╚═╝╚══════╝╚══════╝          "
    "╚═╝╚═╝  ╚═══╝ ╚═════╝",
    "",
    "",
    "                                ──『 TEAM OTAKU 』──",
    "                           mramaros      &&      raaron-v",
]


def check_the_repetitives(
    key: str, pre_dict: list[str], sms: list[str]
) -> None:
    """
    Check for repetitive keys in the configuration dictionary.

    Args:
        key (str): The configuration key to check for duplicates.
        pre_dict (list[str]): The raw list of configuration strings.
        sms (list[str]): A list used to append warning messages.
    """
    count = 0

    for pseudo_key in pre_dict:
        name, content = pseudo_key.split("=", 1)
        if key == name:
            count += 1

    if count > 1:
        sms.append(f"[WARNING] This key:'{key}' is repetitive x{count}")


def read_config(the_file: str) -> list[str]:
    """
    Read a configuration file and return its lines stripped of newlines.

    Args:
        the_file (str): The path to the configuration file.

    Returns:
        list[str]: A list containing the processed lines of the file.
    """
    config = []
    with open(the_file, "r") as res:
        for line in res:
            config.append(line.rstrip("\n"))
    return config


def input_the_congif_maze(the_file: str) -> list[str]:
    """
    Input the configuration for the maze from a specific file.

    Args:
        the_file (str): The path to the configuration file.

    Returns:
        list[str]: A list containing the read lines of the configuration file.
    """
    return read_config(the_file)


def take_config(argv: str, sms: list[str]) -> dict[str, str]:
    """
        Parse the configuration file and extract settings into a dictionary.

        Args:
            argv (str): The path to the configuration file to be read.
            sms (list[str]): A list to collect warning messages for
                repetitive keys.

        Raises:
            SyntaxError: If a configuration line has invalid syntax or
                empty values.
            ValueError: If an unrecognized key is present in the configuration.

        Returns:
            dict[str, str]: A dictionary containing the parsed key-value pairs.
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
                "There is a small syntax error in your "
                f"configuration file, here {tmp}"
            )

    for tmp in true_config:
        name, content = tmp.split("=", 1)
        check_the_repetitives(name, true_config, sms)
        the_dict[name.strip()] = content

    for one, two in the_dict.items():
        if one != "seed":
            if len(one) == 0 or len(two) == 0:
                raise SyntaxError(
                    f"that syntax key = '{one}' or/"
                    f"and value = '{two}' is incorrect."
                )

    list_key = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "seed",
        "ALGO",
        "DISPLAY",
        "ANIMATION",
        "SPEED",
        "ALGO_SOLVE",
        "SMS"
    ]
    for the_key in the_dict.keys():
        if the_key not in list_key:
            raise ValueError(
                f"This key: '{the_key}' and its value: '{the_dict[the_key]}'"
                " is useless\n Please remove it from your configuration file"
            )

    return the_dict


cell_size = 20
outline_thickness = 3

if __name__ == "__main__":
    try:
        sms_for_duplicate: list[str] = []
        cols = 0
        rows = 0
        list_color = [
            0x11FFFFFF,
            0x1100FFFF,  # Cyan
            0x11FFFF00,  # Jaune
            0x110000FF,  # Bleu
            0x1187CEEB,  # Bleu ciel
            0x11FFA500,  # Orange
            0x11FF69B4,  # Rose
            0x11800080,  # Violet
            0x11FF0000,
            0x11FF00FF,
            0x1100FFFF,
            0x11FF7F7F,  # Rouge clair
            0x1190EE90,  # Vert clair
        ]

        color = random.choice(list_color)
        color_iso = random.choice(list_color)

        if len(sys.argv) == 2:
            the_dict = take_config(sys.argv[1], sms_for_duplicate)
        else:
            raise SystemExit(
                "There is an error in the way you are launching the program"
                "\n     Usage: python a_maze_ing.py <config_file>"
            )

        if "WIDTH" in the_dict and "HEIGHT" in the_dict:
            width = int(the_dict["WIDTH"])
            height = int(the_dict["HEIGHT"])

            old_cell_size = 20
            nb_cols = width
            nb_rows = height

            max_screen_width = 1700
            max_scree_height = 900

            ideal_w = max_screen_width // nb_cols if nb_cols > 0 else 36
            ideal_h = max_scree_height // nb_rows if nb_rows > 0 else 36

            cell_size = min(ideal_w, ideal_h, 50)

            if cell_size < 4:
                cell_size = 4
            outline_thickness = max(1, int(cell_size * 0.12))

            cols = width * cell_size + outline_thickness
            rows = height * cell_size + outline_thickness

            if width < 9 or height < 8:
                tmp_err = "[WARNING] Pattern '42' is too large for a "
                tmp_err += "maze with a width < 9 or a height < 8"
            if width * height <= 1:
                raise ValueError(
                    "The WIDTH or height you provided is too small"
                    " to create a maze\n(Note: WIDTH * HEIGHT >= 2)"
                )
            if height > 220:
                raise ValueError("the HEIGHT is too high, max: 220")
            if width > 300:
                raise ValueError("the WIDTH is too high, max: 300")
            if width * height > 66000:
                raise ValueError("trop")

        else:
            raise ValueError(
                "The WIDTH or HEIGHT configurations do not exist"
            )

        if "ENTRY" in the_dict and "EXIT" in the_dict:
            tmp_ent_x, tmp_ent_y = the_dict["ENTRY"].split(",", 1)
            tmp_int_ent_x = int(tmp_ent_x)
            tmp_int_ent_y = int(tmp_ent_y)
            entry_x_px = tmp_int_ent_x * cell_size + outline_thickness
            entry_y_px = tmp_int_ent_y * cell_size + outline_thickness
            tuple_entry = (tmp_int_ent_x, tmp_int_ent_y)

            tmp_exi_x, tmp_exi_y = the_dict["EXIT"].split(",", 1)
            tmp_int_exi_x = int(tmp_exi_x)
            tmp_int_exi_y = int(tmp_exi_y)
            exit_x_px = tmp_int_exi_x * cell_size + outline_thickness
            exit_y_px = tmp_int_exi_y * cell_size + outline_thickness
            tuple_exit = (tmp_int_exi_x, tmp_int_exi_y)

            if tuple_entry == tuple_exit:
                raise ValueError(
                    "the coordinates of the ENTRY and EXIT are identical"
                )
        else:
            raise ValueError("The ENTRY or EXIT configurations do not exist")

        if tmp_int_ent_x < 0 or tmp_int_ent_x >= width:
            raise ValueError("ENTRY x-coordinate outside field.")
        elif tmp_int_ent_y < 0 or tmp_int_ent_y >= height:
            raise ValueError("ENTRY y-coordinate outside field.")

        if tmp_int_exi_x < 0 or tmp_int_exi_x >= width:
            raise ValueError("EXIT x-coordinate outside field.")
        elif tmp_int_exi_y < 0 or tmp_int_exi_y >= height:
            raise ValueError("EXIT y-coordinate outside field.")

        Algo = 1
        if "ALGO" in the_dict:
            Algo = int(the_dict["ALGO"])

        Algo_solve = 0
        if "ALGO_SOLVE" in the_dict:
            Algo_solve = int(the_dict["ALGO_SOLVE"])
            if Algo_solve not in (1, 2):
                Algo_solve = 0

        if "PERFECT" in the_dict:
            if the_dict["PERFECT"].strip().capitalize() == "False":
                perfect = False
            elif the_dict["PERFECT"].strip().capitalize() == "True":
                perfect = True
            else:
                raise ValueError("The value of PERFECT is invalid")
        else:
            raise ValueError("The PERFECT configurations do not exist")

        res_seed = None
        if "seed" in the_dict:
            res_seed = the_dict["seed"]

        display_sms = [False]
        if "SMS" in the_dict:
            if the_dict["SMS"].strip().capitalize() == "True":
                display_sms[0] = True

        display = [False]
        if "DISPLAY" in the_dict:
            if the_dict["DISPLAY"].strip().capitalize() == "True":
                display[0] = True

        animate_gen = False
        if "ANIMATION" in the_dict:
            if the_dict["ANIMATION"].strip().capitalize() == "True":
                animate_gen = True

        the_speed = 4
        if "SPEED" in the_dict:
            the_speed = int(the_dict["SPEED"])

        our_a_maze_ing = MazeGenerator(
            width, height, tuple_entry, tuple_exit, res_seed
        )
        our_a_maze_ing.create_all_cells()
        if width >= 9 and height >= 8:
            the_isolateds = our_a_maze_ing.isolated_cells()

            if tuple_entry in the_isolateds:
                raise ValueError(
                    "The ENTRY point is located in one of the isolated cells"
                    "\nThis action is impossible because the isolated cells "
                    "are and will always remain closed"
                )
            if tuple_exit in the_isolateds:
                raise ValueError(
                    "The EXIT point is located in one of the isolated cells"
                    "\nThis action is impossible because the isolated cells "
                    "are and will always remain closed"
                )

        if Algo == 1:
            the_maze = our_a_maze_ing.generated_maze_dfs()
        elif Algo == 2:
            the_maze = our_a_maze_ing.generated_maze_prim_s()
        else:
            raise ValueError(
                "This algorithm (or this algorithm reference) does not exist."
            )

        if not perfect:
            for a_cell in our_a_maze_ing.all_cell:
                our_a_maze_ing.imperfect_maze(a_cell)

        if perfect or Algo_solve == 1:
            solver = our_a_maze_ing.solver_dfs(
                entry_x_px,
                entry_y_px,
                exit_x_px,
                exit_y_px,
                outline_thickness,
                cell_size,
            )
        elif not perfect or Algo_solve == 2:
            solver = our_a_maze_ing.solver_bfs(
                entry_x_px,
                entry_y_px,
                exit_x_px,
                exit_y_px,
                outline_thickness,
                cell_size,
            )
        nesw = solver_in_nesw(solver)

        the_maze_in_hexa = []
        for y in range(our_a_maze_ing.height):
            line = ""
            for x in range(our_a_maze_ing.width):
                line += our_a_maze_ing.get_cell(x, y).hex_char()
            the_maze_in_hexa.append(line)

        try:
            if "OUTPUT_FILE" in the_dict:
                with open(the_dict["OUTPUT_FILE"].strip(), "w") as out:
                    for string in the_maze_in_hexa:
                        out.write(string + "\n")
                    out.write("\n")
                    out.write(
                        f"{our_a_maze_ing.entry[0]},"
                        f"{our_a_maze_ing.entry[1]}\n"
                    )
                    out.write(
                        f"{our_a_maze_ing.exit[0]},{our_a_maze_ing.exit[1]}\n"
                    )
                    for cha in nesw:
                        out.write(cha)
                    out.write("\n")
            else:
                raise ValueError(
                    "the OUTPUT_FILE configurations do not exist"
                )
        except Exception as e:
            sys.exit(str(e))

        try:
            print()
            for char in title:
                print(char)

            print("\n")
            space = "          " * 2

            print(f"{space} ⎡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⎤")
            print(f"{space}                MAZE CONFIG")
            print(f"{space} ⎪ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⎪\n")
            print(f"{space}         • WIDTH          → {width}")
            print(f"{space}         • HEIGTH         → {height}")
            print(f"{space}         • ENTRY (x, y)   → {tuple_entry}")
            print(f"{space}         • EXIT (x, y)    → {tuple_exit}")
            print(f"{space}         • ALGO           → {Algo}")
            print(f"{space}         • PERFECT        → {perfect}\n")
            print(f"{space} ⎣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⎦")

            if width < 9 or height < 8:
                print()
                print(f"    {tmp_err}")
            if len(sms_for_duplicate) != 0:
                space = " " * 17
                print()
                print(f"{space}   {sms_for_duplicate[0]}")

            from mazegen import MazeMlx, anime
            from mazegen.key_maps import (
                custom_handle_keypress,
                custom_handle_mouse,
            )

            gamer_state = GameState(tuple_entry, tuple_exit)
            my_window = MazeMlx(
                cols, rows, width, height, cell_size, outline_thickness
            )

            my_window.mlx.mlx_put_image_to_window(
                my_window.mlx_ptr, my_window.win, my_window.img, 15, 15
            )

            show_solver = [0]
            color_ref = [color]
            isolated_list = list(our_a_maze_ing.all_isolated)
            isoler_original = list(our_a_maze_ing.all_isolated)

            start_screen = [True]
            box_bounds = [0, 0, 0, 0]
            start_printed = [False]
            already_printed = [False]
            only_once = [False]

            state: dict[str, Any] = {
                "tmp_sms": display_sms,
                "Algo_solve": Algo_solve,
                "class maze": our_a_maze_ing,
                "true_entry": tuple_entry,
                "display": display[0],
                "WIDTH": width,
                "HEIGHT": height,
                "anime": the_maze,
                "isoler": isolated_list,
                "isoler_original": isoler_original,
                "solver": [solver],
                "show_solver": show_solver,
                "color": color_ref,
                "color_iso": color_iso,
                "list_color": list_color,
                "my_window": my_window,
                "all_cell": our_a_maze_ing.all_cell,
                "ENTRY_X": [entry_x_px],
                "ENTRY_Y": [entry_y_px],
                "EXIT_X": exit_x_px,
                "EXIT_Y": exit_y_px,
                "start_screen": start_screen,
                "box_bounds": box_bounds,
                "start_printed": start_printed,
                "already_printed": already_printed,
                "gamer_state": gamer_state,
            }
            tmp_all_cell = list(our_a_maze_ing.all_cell)

            my_window.mlx.mlx_loop_hook(
                my_window.mlx_ptr,
                lambda _: anime(
                    display,
                    display_sms,
                    our_a_maze_ing,
                    the_maze,
                    state["solver"][0],
                    len(state["solver"][0]),
                    my_window,
                    our_a_maze_ing.all_cell,
                    tmp_all_cell,
                    [perfect],
                    isolated_list,
                    color_ref,
                    color_iso,
                    list_color,
                    width,
                    height,
                    state["ENTRY_X"][0],
                    state["ENTRY_Y"][0],
                    exit_x_px,
                    exit_y_px,
                    cols,
                    rows,
                    already_printed,
                    only_once,
                    show_solver,
                    start_screen,
                    box_bounds,
                    start_printed,
                    animate_gen,
                    the_speed,
                ),
                None,
            )

            my_window.mlx.mlx_hook(
                my_window.win,
                2,
                1,
                lambda keycode, *args: custom_handle_keypress(keycode, state),
                None,
            )

            my_window.mlx.mlx_mouse_hook(
                my_window.win,
                lambda button, x, y, *args: custom_handle_mouse(
                    button, x, y, state
                ),
                None,
            )

            my_window.mlx.mlx_hook(
                my_window.win,
                33,
                0,
                lambda _: my_window.mlx.mlx_loop_exit(my_window.mlx_ptr),
                None,
            )

            my_window.mlx.mlx_loop(my_window.mlx_ptr)
        except Exception as e:
            print(f"MLX er not started: {e}")

    except ValueError as e:
        print(f"[WARNING] ValueError: {e}")
    except TypeError as e:
        print(f"[WARNING] A TypeError: {e}")
    except IndexError as e:
        print(f"[WARNING] A IndexError: {e}")
    except KeyError as e:
        print(f"[WARNING] A KeyError: {e}")
    except Exception as e:
        print(f"An error (Exception) has occurred: {e}")
        print(e)
    except SystemExit as e:
        print(f"[WARNING] A SystemExit: {e}")
    except KeyboardInterrupt:
        print("[WARNING] you are user ctrl + C")
