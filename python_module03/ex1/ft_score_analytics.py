#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Player Score Analytics ===")

    raw_argv = sys.argv[1:]

    if not raw_argv:
        print("No scores provided. Usage: python3", end="")
        print("ft_score_analytics.py <score1> <score2> ...")
        return

    score: list[int] = []

    for i in raw_argv:
        try:
            input = int(i)
            score.append(input)
        except ValueError:
            print(f"Invalid parameter: '{i}'")

    if not score:
        print("No scores provided.", end="")
        print(" Usage: python3 ft_score_analytics.py <score1> <score2> ...")

    else:
        total_player = len(score)
        total_score = sum(score)
        average_score = total_score / total_player
        high_score = max(score)
        low_score = min(score)
        score_range = high_score - low_score

        print(f"Scores processed: {score}")
        print(f"Total players: {total_player}")
        print(f"Total score: {total_score}")
        print(f"Average score: {average_score}")
        print(f"High score: {high_score}")
        print(f"Low score: {low_score}")
        print(f"Score_range: {score_range}")


if __name__ == "__main__":
    main()
