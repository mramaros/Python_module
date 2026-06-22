from ex0.creature import creature


class Flameling(creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(slef) -> str:
        return "Flameling uses Ember!"


class Pyrodon(creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return "Pyrodon uses Flamethrower!"


class Aquabub(creature):
    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        return "Aquabub uses Water Gun!"



class Torragon(creature):
    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        return ("Torragon uses Hydro Pump!")
