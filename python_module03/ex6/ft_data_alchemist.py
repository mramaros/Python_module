#!/usr/bin/env python3

import random


def main() -> None:
    print("=== Game Data Alchemist ===")

    players: list[str] = {
            "Alice", "bob", "Charlie", "dylan", "Emma", "Gregory", "john", "kevin", "Liam"
            }

    print(f"Initial list of players: {players}")

    all_capitalized = [name.capitalize() for name in players]

    print(f"New list for capitalized only: {all_capitalized}")

    all_nocapitalized = [name for name in players if name[0].isupper()]

    print(f"New list of capitalized names only: {all_nocapitalized}")

    score = {name: random.randint(0, 1000) for name in all_capitalized}
    print(f"Score dict: {score}")
    
    average = sum(score.values()) / len(score)
    print(f"Score average is: {average:.2f}")

    high_score = {}
    for name, scores in score.items():
        if scores > average:
            high_score[name] = scores

    print(f"High scores: {high_score}")


if __name__ == "__main__":
    main()
