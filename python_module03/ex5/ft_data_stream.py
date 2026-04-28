#!/usr/bin/env python3

from typing import Generator
import random


def  gen_event () -> Generator[tuple[str, str], None, None]:
    players = ["Alice", "Bob", "Dylan", "Charlie"]
    action = ["run", "eat", "sleep", "grab", "move", "swim", "climb",
              "release"]

    while True:
        yield (random.choise(players), random.choise(action))


def consume_event() -> None:
    


if __name__ == "__main__":
    main()
