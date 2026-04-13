# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_analytics.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mramaros <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/12 23:08:00 by mramaros          #+#    #+#              #
#    Updated: 2026/04/13 07:10:23 by mramaros         ###   ########.fr        #
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

def set_height(height, value)-> None:
    self._height = float(value)

def set_age
