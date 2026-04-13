# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_analytics.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/12 23:08:00 by mramaros          #+#    #+#              #
#    Updated: 2026/04/13 08:07:29 by mramaros         ###   ########.fr        #
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
        self._heiht = 0
        self.set_height(height)
        self.set_age(age)

    @classmethode
    def unonynous(cls):
        return cls("Unknow types", 0, 0)

    @staticmethode
    def is_older_than_a_year(age)
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


