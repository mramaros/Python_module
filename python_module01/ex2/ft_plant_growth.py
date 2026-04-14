#!/usr/bin/env python3
 
 
class Plant():
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.age: int = 0
 
    def grow(self) -> None:
        self.height = self.height + 0.8
 
    def age_plant(self) -> None:
        self.age = self.age + 1
 
    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, "
              f"{self.age} days old")


if __name__ == "__main__":
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.age = 30

    initial_height = rose.height

    print("=== Garden Plant Growth ===")
    rose.show()

    for i in range(1, 8):
        rose.grow()
        rose.age_plant()
        print(f"=== Day {i} ===")
        rose.show()

    growth = round(rose.height - initial_height, 1)
    print(f"Growth this week: {growth}cm")
