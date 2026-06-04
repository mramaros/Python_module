#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Inventory System Analysis ===")

    raw_args = sys.argv[1:]
    if not raw_args:
        print("At the beginning of the game,", end="")
        print("your inventory is usually empty ;)")
        return

    invetory: dict[str, int] = {}

    for arg in raw_args:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue

        item, quantity_str = arg.split(":", 1)
        if not item:
            print(f"\nError message: '{item}' is a empty value\n")
            break

        if item in invetory:
            print(f"Reduntant item '{item}' - discarding")
            continue

        try:
            quantity = int(quantity_str)
            invetory[item] = quantity
        except ValueError as e:
            print(f"Quality error for '{item}': {e}")

    if not invetory:
        return

    print(f"Got inventory: {invetory}")

    items_list = list(invetory.keys())

    print(f"Item list: {items_list}")

    total_quantity = sum(invetory.values())
    print(f"Total quantity of the {len(items_list)} items: {total_quantity}")

    for item, quantity in invetory.items():
        try:
            percentage = (quantity / total_quantity) * 100
        except Exception:
            percentage = 0
        print(f"Item {item} represents {percentage:.1f}%")

    most_abondant = items_list[0]
    less_abondant = items_list[0]

    for item in items_list:
        if invetory[item] > invetory[most_abondant]:
            most_abondant = item

        if invetory[item] < invetory[less_abondant]:
            less_abondant = item

    print(f"Item most abundant: {most_abondant}", end="")
    print(f" with quantity {invetory.get(most_abondant)}")
    print(f"Item least abundant: {less_abondant} ", end="")
    print(f"with quantity {invetory.get(less_abondant)}")

    invetory["magic_item"] = 1

    print(f"Updated inventory: {invetory}")


if __name__ == "__main__":
    main()
