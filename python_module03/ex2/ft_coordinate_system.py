#!/usr/bin/env python3

import math

def get_pos() -> tuple[float, float, float]:
    while True:
        try:
            line = input("Enter new coordinates as floats in format 'x,y,z': ")

            part = line.split(",")

            if len(part) != 3:
                print("Invalid Syntax")
                continue

            x = float(part[0].strip())
            y = float(part[1].strip())
            z = float(part[2].strip())

            return (x, y, z)

        except ValueError as e:
            print(f"Error: {e}")


def main() -> None:
    print("=== Game Coordinate System ===")

    print("\nGet a first set of coordinates")
    pos1 = get_pos()

    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_center = math.sqrt(pos1[0]**2 + pos1[1]**2 + pos1[2]**2)
    print(f"Distance to center: {dist_center:.4f}")

    print("\nGet a second set of coordinates")
    pos2 = get_pos()

    dist_between = math.sqrt((pos2[0] - pos1[0])**2 +
                             (pos2[1] - pos1[1])**2 +
                             (pos2[2] - pos1[2])**2)
    print(f"Distance between the 2 sets of coordinates: {dist_between:.4f}")


if __name__ == "__main__":
    main()
