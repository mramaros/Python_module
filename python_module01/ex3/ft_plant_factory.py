#!/usr/bin/env python3

class Plant():
    def show(self):
        print(f"{self.name}: {round(self.height, 1)}cm, {self.age} days old")

    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def grow(self):
        self.height = self.height + 0.8


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25.0, 30)
    print("Created:", end=" ")
    rose.show()
    Dak = Plant("Dak", 200.0, 365)
    print("Created:", end=" ")
    Dak.show()
    Cactus = Plant("Cactus", 5.0, 90)
    print("Created:", end=" ")
    Cactus.show()
    Sunflower = Plant("Sunflower", 80.0, 45)
    print("Created:", end=" ")
    Sunflower.show()
    Fern = Plant("Fern", 15.0, 120)
    print("Created:", end=" ")
    Fern.show()
