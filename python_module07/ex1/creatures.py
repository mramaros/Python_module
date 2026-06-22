from ex0.creature import creature
from ex1.capabilities import HealCapability, TransformCapability

class Sproutling(creature, HealCapability):
    def __init__(self) -> None:
        creature.__init__(self, "Sproutling", "Grass")

    def attack(self) -> str:
        return "Sproutling uses Vine Whip!"

    def heal(self) -> str:
        return "Sproutling heals itself for a small amount"


class Bloomelle(creature, HealCapability):
    def __init__(self) -> None:
        creature.__init__(self, "Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        print("Bloomelle uses Petal Dance!")

    def heal(self) -> str:
        return "Bloomelle heals itself and others for a large amount"


class Shiftling(creature, TransformCapability):
    def __init__(self) -> None:
        creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return "Shiftling performs a boosted strike!"
        return "Shiftling attacks normally."

    def transforme(self) -> str:
        self.transformed = True
        return "Shiftling shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return "Shiftling returns to normal."


class Morphagon(creature, TransformCapability):
    def __init__(self) -> None:
        creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return "Morphagon unleashes a devastating morph strike!"
        return "Morphagon attacks normally."

    def transforme(self) -> str:
        self.transformed = True
        return "Morphagon morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.transformed = False
        return "Morphagon stabilizes its form."
