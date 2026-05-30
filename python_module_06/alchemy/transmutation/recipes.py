from elements import create_fire
from ..potions import strength_potion
from ..elements import create_air

def lead_to_gold():
    return (
            "Recipe transmuting Lead to Gold: brew "
            f"'{create_air()}' and '{strength_potion()}' mixed with '{create_fire()}'"
            )
