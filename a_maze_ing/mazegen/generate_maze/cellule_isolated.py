def isolated_cells(WIDTH, HEIGHT) -> set:
    """
    Retourne un ensemble de coordonnées (x,y) représentant les cellules isolées.
        Celui de "42" principalement, mais aussi d'autres cellules autour de celle-ci.
    Ces cellules ne seront pas visitées lors de la génération du labyrinthe.
    """
    return {
        (WIDTH // 2 - 1, HEIGHT // 2),
        (WIDTH // 2 - 2, HEIGHT // 2),
        (WIDTH // 2 - 3, HEIGHT // 2),
        (WIDTH // 2 + 1, HEIGHT // 2),
        (WIDTH // 2 + 2, HEIGHT // 2),
        (WIDTH // 2 + 3, HEIGHT // 2),
        (WIDTH // 2 - 3, HEIGHT // 2 - 1),
        (WIDTH // 2 - 3, HEIGHT // 2 - 2),
        (WIDTH // 2 - 1, HEIGHT // 2 + 1),
        (WIDTH // 2 - 1, HEIGHT // 2 + 2),
        (WIDTH // 2 + 1, HEIGHT // 2 + 1),
        (WIDTH // 2 + 1, HEIGHT // 2 + 2),
        (WIDTH // 2 + 3, HEIGHT // 2 - 1),
        (WIDTH // 2 + 3, HEIGHT // 2 - 2),
        (WIDTH // 2 + 2, HEIGHT // 2 - 2),
        (WIDTH // 2 + 1, HEIGHT // 2 - 2),
        (WIDTH // 2 + 2, HEIGHT // 2 + 2),
        (WIDTH // 2 + 3, HEIGHT // 2 + 2),
    }