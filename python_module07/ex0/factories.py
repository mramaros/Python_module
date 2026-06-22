from abc import ABC, abstractmethod
from ex0.creature import creature
from ex0.creatures import Flameling, Pyrodon, Aquabub, Torragon


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> creature:
        pass

    def create_evolved(self) -> creature:
        pass


class FlameFactory(CreatureFactory):
    def  create_base(self) -> creature:
        return Flameling()

    def create_evolved(self) -> creature:
        return Pyrodon()


class AquaFactory(CreatureFactory):
    def create_base(self) -> creature:
        return Aquabub()

    def create_evolved(self) -> creature:
        return Torragon()
