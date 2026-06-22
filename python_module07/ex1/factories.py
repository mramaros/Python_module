from ex0.factories import CreatureFactory
from ex0.creature import creature
from ex1.creatures import Sproutling, Bloomelle, Shiftling, Morphagon


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> creature:
        return Sproutling()

    def create_evolved(self) -> creature:
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> str:
        return Shiftling()

    def create_evolved(self) -> creature:
        return Morphagon()
