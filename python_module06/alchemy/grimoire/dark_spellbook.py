from alchemy.grimoire.light_validator import validate_ingredients

def  dark_spell_allowed_ingredients() -> list[str]:
    return [
        "bats",
        "frogs",
        "arsenic",
        "eyeball"
        ]

def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result :str = validate_ingredients(ingredients)

    if "INVALID" == result:
        return f"Spell rejected : {ingredients} {result}"
    return f"Spell recorded : {ingredients} {result}"
