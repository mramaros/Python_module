
def validate_ingredients(ingredients: str) -> str:
    from alchemy.grimoire.light_spellbook import light_spell_allowed_ingredient

    validate_ingredients: list[str] = light_spell_allowed_ingredients()

    for valide in validate_ingredients:
        if valide in ingredients:
            return f"VALID - {ingredients}"
    return f"INVALID - {ingredients}"
