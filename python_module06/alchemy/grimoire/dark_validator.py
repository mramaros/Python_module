def validate_ingredients(ingredients: str) -> str:
        from alchemy.grimoire.dark_spellbook import (  # noqa: F401
        dark_spell_allowed_ingredients
    )

    validate_ingredients: list[str] = dark_spell_allowed_ingredients()

    for valide in validate_ingredients:
        if valide == ingredients:
            return "VALID"
    return "INVALID"
