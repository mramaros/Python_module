class Plant():
    def __init__(self, name, height, age):
        self._name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> int:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, value) -> None:
        self._height = float(value)

    def set_age(self, value) -> None:
        self._age = value

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")

    def grow(self, amount=1.0) -> None:
        self.set_height(self._height + amount)

    def age(self, days=1) -> None:
        self.set_age(self._age + days)


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self._color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._blooming:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self._trunk_diameter = float(trunk_diameter)

    def produce_shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {round(self._trunk_diameter, 1)}cm")


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season):
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = 0

    def grow(self, amount=1.0) -> None:
        super().grow(amount)

    def age(self, days=1) -> None:
        super().age(days)
        self._nutritional_value += 1

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    print("\n=== Flower")
    rose = Flower("Rose", 15, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("\n=== Tree")
    oak = Tree("Oak", 200, 365, 5)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for i in range(20):
        tomato.grow(2.1)
        tomato.age(1)
    tomato.show()
