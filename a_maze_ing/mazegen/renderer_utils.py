"""Sprite and theme utility module.

This module provides helper functions for extracting, scaling, and
recoloring sprite images. It also defines the color themes used for
maze floors, walls, and background rendering.
"""

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

from .spritsheet import Spritesheet


def tileset(
            x_coordinates: tuple[int, int],
            y_coordinates: tuple[int, int],
            spritesheet: Spritesheet
        ) -> tuple[np.ndarray, int, int]:
    """Extract a sprite from a spritesheet."""
    x_min, x_max = x_coordinates
    y_min, y_max = y_coordinates
    tileset = spritesheet.get_tileset(x_min, x_max, y_min, y_max)
    tileset_height, tileset_width, _ = tileset.shape
    return (tileset.copy(), tileset_height, tileset_width)


def scale_pixel(sprite: np.ndarray, scale: int) -> np.ndarray:
    """Scale a sprite using nearest-neighbor enlargement."""
    scaled_img = np.repeat(sprite, scale, axis=0)
    scaled_img = np.repeat(scaled_img, scale, axis=1)
    return scaled_img


def recolor_pixel(
        sprite: np.ndarray,
        target_color: list[int],
        new_color: list[int]
) -> None:
    """Replace a color within a sprite."""
    mask = np.all(sprite == target_color, axis=2)
    sprite[mask] = new_color


# ── Actual RGBA pixel values found in tileset.png ────────────────────────────
# These are the 3 recolorable layers of the wall sprites:
#   WALL_PRIMARY  = (66,  40, 53,  255)  <- main brick face
#   WALL_SHADOW   = (28,  17, 23,  255)  <- deep shadow / mortar
#   WALL_HIGHLIGHT = (117, 103, 96, 255)  <- edge highlight


floor_colors: dict[str, list[list[int]]] = {
    # ── Dungeon: dark stone earth, near-black corridors ───────────────────
    "default_theme": [
        [ 40,  40,  24, 255],   # f1 dark earth floor
        [ 56,  56,  40, 255],   # f2 slightly lighter stone
        [180,  90,  20, 255],   # f3 path highlight (torch orange)
    ],

    # ── Ice cavern: cold steel-blue ice corridors ─────────────────────────
    "ice_theme": [
        [104, 152, 184, 255],   # f1 deep ice blue
        [184, 216, 232, 255],   # f2 pale ice surface
        [ 60, 220, 255, 255],   # f3 path highlight (bright cyan)
    ],

    # ── Desert ruins: warm sand, compacted dirt corridors ────────────────
    "desert_theme": [
        [152, 104,  56, 255],   # f1 compacted sand
        [200, 152,  80, 255],   # f2 pale sandstone floor
        [255, 200,  40, 255],   # f3 path highlight (sun gold)
    ],

    # ── Garden: rich earth-brown soil corridors ───────────────────────────
    "garden_theme": [
        [120,  88,  40, 255],   # f1 dark soil
        [104, 120,  32, 255],   # f2 mossy earth
        [160, 230,  60, 255],   # f3 path highlight (bright leaf)
    ],
}

wall_colors: dict[str, list[list[int]]] = {
    # Each entry: [new_primary, new_shadow, new_highlight]
    # replacing   [66,40,53],  [28,17,23],  [117,103,96]  respectively

    # ── Dungeon: charcoal stone, near-black mortar, pale stone highlight ──
    "default_theme": [
        [ 45,  38,  30, 255],   # dark stone face
        [  8,   8,   8, 255],   # near-black mortar / deep shadow
        [100,  95,  80, 255],   # worn stone highlight
    ],

    # ── Ice: steel blue stone, midnight shadow, brilliant ice highlight ───
    "ice_theme": [
        [110, 155, 185, 255],   # cold blue stone face
        [ 55,  90, 130, 255],   # deep ice shadow
        [215, 240, 252, 255],   # glinting ice highlight
    ],

    # ── Desert: warm sandstone face, deep ochre shadow, sun-bleached top ─
    "desert_theme": [
        [168, 112,  52, 255],   # sandstone brick face
        [ 96,  56,  20, 255],   # deep ochre shadow / crack
        [232, 185, 110, 255],   # sun-bleached highlight
    ],

    # ── Garden: deep hedge green, near-black undergrowth, bright foliage ─
    "garden_theme": [
        [ 72,  96,  24, 255],   # dense hedge face
        [ 28,  44,   8, 255],   # dark undergrowth shadow
        [104, 152,  32, 255],   # bright leaf highlight
    ],
}

background_colors: dict[str, list[int]] = {
    "default_theme": [ 18,  16,  14, 255],   # near-black dungeon void
    "ice_theme":     [168, 210, 230, 255],   # deep glacial blue
    "desert_theme":  [184, 128,  56, 255],   # warm desert dusk
    "garden_theme":  [ 30,  45,  10, 255],   # dark forest undergrowth
}
