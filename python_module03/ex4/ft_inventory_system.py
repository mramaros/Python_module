#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Inventory System Analysis ===")

    raw_args = sys.argv[1:]
    if not raw_args:
        print("sorry, during the game, your invetory is actually empty ;)")
        return

    invetory: dict[str, int] = {}

    for arg in raw_args:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue

        item, quantity_str = arg.split(":", 1)
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
        percentage = (quantity / total_quantity) * 100
        print(f"Item {item} represents {percentage:.1f}%")

    max_nbr_item = max(invetory, key=invetory.get)
    min_nbr_item = min(invetory, key=invetory.get)

    print(f"Item most abundant: {item} with quantity {max_nbr_item}")
    print(f"Item least abundant: {item} with quantity {min_nbr_item}")

    print(f"Updated inventory: {invetory}")



if __name__ == "__main__":
    main()
