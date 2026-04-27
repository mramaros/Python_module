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

    player : dict[str, set[str]] = {
        "Alice" : gen_player_achievements(),
        "BOb" : gen_player_achievements(),
        "Charlie" : gen_player_achievements(),
        "Dylan" : gen_player_achievements(),
        "Dylan" : gen_player_achievements()
    }

    for name, achivement in player.items():
        print(f"Player {name}: {achivement}")

    all_distinct = (player["Alice"] | player["Bob"] | 
                    player["Charlie"] | player["Dylan"])

    print("\nAll distinct achivements: {all_distinct}")

    common = (player["Alice"] & player["Bob"] &
            player["Charlie"] & player["Dylan"])
    print(f"Common achivement: {common}")

#    for name, current_set in player.items():
#        others = [s for n, s in player.items() if n != name]
#        other_union = set().union(*others)
#        only_this_player = current_set - other_union
#        print(f"Only{name} has: {only_this_player if only_this_player else 'set()'}")

    for name, current_set in player.items():
        missing = all_distinct - current_set
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
