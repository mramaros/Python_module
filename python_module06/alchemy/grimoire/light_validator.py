
def validate_ingredients(ingredients: str) -> str:
    from alchemy.grimoire.light_spellbook import light_spell_allowed_ingredients

    allowed_ingredients: list[str] = light_spell_allowed_ingredients()

    normalized = ingredients.lower()
    # Treat common synonym 'wind' as 'air' so phrases like
    # 'Earth, wind and fire' validate correctly.
    normalized = normalized.replace("wind", "air")

    for candidate in allowed_ingredients:
        if candidate in normalized:
            return "VALID"
    return "INVALID"
