"""Minimal spritesheet helper used by the renderer.

Provides a lightweight `Spritesheet` class with `get_tileset()` that
returns an RGBA numpy sub-array from a full tileset image.
"""
from typing import Any


class Spritesheet:
    def __init__(self, img_3d: Any) -> None:
        self.img = img_3d

    def get_tileset(self, x_min: int, x_max: int, y_min: int, y_max: int):
        return self.img[y_min:y_max, x_min:x_max]
