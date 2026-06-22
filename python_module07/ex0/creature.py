from abc import ABC, abstractmethod

class creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name:str = name
        self.creature_type:str = creature_type

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type creature"

    @abstractmethod
    def attack(self) -> str:
        pass
