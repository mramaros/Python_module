#!/usr/bin/env python3


class Plant():
    def __init__(self, name, height, age):
        self._name = name
        self._height = 0.0
        if height > 0.0:
            self._height = height
        self._age = 0
        if age > 0:
            self._age = age

    def get_height(self) -> int:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, value) -> None:
        if (value < 0):
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = value
            print(f"Height updated: {self._height}cm")

    def set_age(self, value) -> None:
        if (value < 0):
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = value
            print(f"Age updated: {self._age}cm")

    def grow(self):
        self.height = self.height + 0.8

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    print("")
    rose = Plant("Rose", 15.0, 10)
    rose.show()
    print("")
    rose.set_height(30)
    rose.set_age(25)
    rose.get_age()
    rose.get_height()
    print("\nPlant created: ", end="")
    rose.set_height(-4)
    rose.set_age(-5)
    rose.get_age()
    rose.get_height()
    print("Current state: ", end="")
    rose.show()
