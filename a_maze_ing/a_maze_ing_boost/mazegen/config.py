#!/usr/bin/env python3
# ########################################################################### #
#   mazegen/config.py                                                         #
# ########################################################################### #


def read_config(the_file: str) -> list:
    config = []
    with open(the_file, "r") as res:
        for line in res:
            config.append(line.rstrip("\n"))
    return config


def input_the_config_maze(the_file: str) -> list:
    return read_config(the_file)


def take_config(argv: str) -> dict:
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

    only_not_vide = [ch for ch in true_config if len(ch) != 0]
    true_config = only_not_vide

    for tmp in true_config:
        if tmp.count("=") != 1:
            raise SyntaxError(
                "There is a small syntax error in your configuration file, "
                f"here {tmp}"
            )

    for tmp in true_config:
        name, content = tmp.split("=", 1)
        the_dict[name] = content

    for one, two in the_dict.items():
        if len(one) == 0 or len(two) == 0:
            raise SyntaxError(
                f"that syntax key = '{one}' or/and value = '{two}' is incorrect."
            )

    return the_dict
