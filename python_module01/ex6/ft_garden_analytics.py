# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_analytics.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/12 23:08:00 by mramaros          #+#    #+#              #
#    Updated: 2026/04/13 17:24:59 by mramaros         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant():
    class Stats:
        def __init__(self):
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def display(self):
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, "
                  f"{self._show_calls} show")

    def __init__(self, name, height, age):
        self._name = name
        self._age = 0
        self._height = 0
        self.set_height(height)
        self.set_age(age)

    @classmethod
    def anonynous(cls):
        return cls("Unknow types", 0, 0)

    @staticmethod
    def is_older_than_a_year(age):
        return age > 365

    def get_age(self)-> int:
        return self._age

    def get_height(self)-> float:
        return self._height

    def set_height(self, value)-> None:
        self._height = float(value)

    def set_age(self, value)-> None:
        self._age = value

    def show(self, amount=1.0)-> None:
        self._stats._grow_calls += 1
        self.set_height(set_height + amount)

    def age(self, days=1)-> None:
        self._stats._age_calls += 1
        self.set_age(set_age + days)

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
    class Stats(Plant.Stats):
        def __init__(self):
            super().__init__()
            self._shade_calls = 0

        def display(self):
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, "
                  f"{self._show_calls} show, "
                  f"{self._shade_calls} shade")

    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, age, height)
        self._trunk_diameter = float(trunk_diameter)
        self._stats = Tree.Stats()

    def produce_shade(self)-> None:
        self._stats._shade_calls += 1
        print(f"Tree {self._name} now produce a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide")

    def show(self)->None:
        super().show()
        print(f"Trunk diameter: {round(self._trunk_diameter, 1)}cm")

Class Seed(Flower):
    def __init__(self, name, height, age, color, seeds=0):
        super().__init__(name, height, age, color)
        self._seeds = seeds

    def show(self)-> None:
        super().show()
        print(f"Seeds: {self._seeds}")

Class Vegetable(Plant):
    def __init__(self, name, age, height, harvest_season):
        super().__init__(name, age, height)
        self._harvest_season = harvest_season
        self._nutrition_value = 0

    def grow(self, amount=1.0)-> None:
        super().grow(amount)

    def age(self)-> None:
        super().age(days)
        print(f"Harvest_season: {self._harvest_season}")
        print(f"Nutrition_value: {self._nutrition_value}")

def display_stats(Plant):
    print(f"[statistic for {self._name}]")
    plant._stats.display()

if __name__ == "__main__":
    print("=== Garden Statics ===")
    print("\n===Check year old")
    print("Is 30 days more than a year? -> "
          f"{Plant.is_older_than_a_year(30)}")
    print("Is 400 days than a year? -> "
          f"{Plant.is_older_than_a_year(400)}")

    print("\n===Flower")
    rose = Flower("Rose", 15, 10, "red")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow(8)
    rose.bloom()
    display_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200 , 365, 5)
    oak.show()
    display_stats(oak)
    print("[Asking the oak to produce the shade]")
    oak.produce_shade()
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "Yellow")

