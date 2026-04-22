#!/usr/bin/env python3

import sys


def main() -> None:
    print("====== Command Quest ===")

    print(f"Program name: {sys.argv[0]}")

    arguments = sys.argv[1:]
    if len(arguments) == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(arguments)}")
        for i, arg in enumerate(arguments, 1):
            print(f"Argument {i}: {arg}")

    print(f"Total arguments: {len(arguments)}")


if __name__ == "__main__":
    main()
