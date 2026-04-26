#!/usr/bin/env python3

import random


def gen_player_achievements() -> set[str]:
    all_achivement: list[str] = [
        "First Steps", "Boss Slayer", "World Savior", "Collector Supreme",
        "Untouchable", "Master Explorer", "Strategist", "Speed Runner",
        "Survivor", "Treasure Hunter", "Sharp Mind", "Hidden Path Finder"
    ]
 
    nb_achivement = random.randint(3, 8)
    selected = random.sample(all_achivement, nb_achivement)
    return set(selected)


def main() -> None:
    print("=== Achievement Tracker System ===")

    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements()
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    all_distinct = (players["Alice"] | players["Bob"] |
                    players["Charlie"] | players["Dylan"])
    print(f"\nAll distinct achievements: {all_distinct}")

    common = (players["Alice"] & players["Bob"] &
              players["Charlie"] & players["Dylan"])
    print(f"Common achievements: {common}")

    for name, current_set in players.items():
        others = [s for n, s in players.items() if n != name]
        others_union = set().union(*others)
        only_this_player = current_set - others_union
        print(f"Only {name} has: {only_this_player if only_this_player else 'set()'}")

    for name, current_set in players.items():
        missing = all_distinct - current_set
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
