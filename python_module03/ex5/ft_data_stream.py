#!/usr/bin/env python3

import typing
from typing import Generator
import random


def  gen_event () -> Generator[tuple[str, str], None, None]:
    players = ["Alice", "Bob", "Dylan", "Charlie"]
    action = ["run", "eat", "sleep", "grab", "move", "swim", "climb",
              "release" ,"use"]

    while True:
        yield (random.choice(players), random.choice(action))


def consume_event(event_list: list[tuple[str, str]]) -> None:
    while len(event_list) > 0:
        index = random.randrange(len(event_list))

        event = event_list.pop(index)

        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    event_stream = gen_event()

    for i in range(1000):
        name, action = next(event_stream)

        if i < 10 or i >990:
            print(f"Event{i}: Player {name} did action {action}")

        elif i == 10:
            print("[...]")

    all_event = [next(event_stream) for _ in range(10)]
    print(f"\nBuilt list of 10 events: {all_event}")

    for event in consume_event(all_event):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {all_event}")


if __name__ == "__main__":
    main()
