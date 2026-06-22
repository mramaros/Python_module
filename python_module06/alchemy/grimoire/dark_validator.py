def validate_ingredients(ingredients: str) -> str:
    from alchemy.grimoire.dark_spellbook import dark_spell_allowed_ingredients  # noqa: F401

    allowed_ingredients: list[str] = dark_spell_allowed_ingredients()

    for valide in allowed_ingredients:
        if valide == ingredients:
            return "VALID"
    return "INVALID"
