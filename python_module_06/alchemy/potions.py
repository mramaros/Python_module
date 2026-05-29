import alchemy.elements
import elements

def healing_potion() -> str:
    return (
            f"Healing potion brewed with '{created_earth()}'"
            f"and '{created_air()}'"
            )


def strength_potion() -> str:
    return (
            f"Strength potion brewed with '{created_fire()}'"
            f"and '{created_water()}'"
            )
