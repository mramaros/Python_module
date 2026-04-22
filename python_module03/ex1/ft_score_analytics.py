#!/usr/bin/env python3

import sys

def main() -> None:
    print("=== Player Score Analytics ===")

    raw_argv = sys.argv[1:]

    if not raw_argv:
        print("No scores provided. Usage: python3" 
            "ft_score_analytics.py <score1> <score2> ...")
    
    score: list[int] = []

    for  i in raw_argv:
        try:
            score = int()


if __name__ == "__main__":
    main()
