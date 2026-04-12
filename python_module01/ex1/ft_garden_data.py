#!/usr/bin/env python3


class Plant:
    def show(self):
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.age = 30
    rose.show()
    Sunflower = Plant()
    Sunflower.name = "Sunflower"
    Sunflower.height = 80
    Sunflower.age = 45
    Sunflower.show()
    Cactus = Plant()
    Cactus.name = "Cactus"
    Cactus.height = 15
    Cactus.age = 120
    Cactus.show()
