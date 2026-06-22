# Maze rendering module (trimmed docstrings to reduce file size)

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

import random
try:
    from ..display_config import DisplayConfig
except Exception:
    from typing import Any as DisplayConfig
from .spritsheet import Spritesheet
from .renderer_utils import (
    scale_pixel,
    recolor_pixel,
    tileset,
    floor_colors,
    wall_colors,
    background_colors
)
from typing import Any


class Draw:
    # Lightweight renderer class (docstrings removed)

    def __init__(
        self,
        img_data: tuple[Any, bytearray, int, int, int],
        buff_data: tuple[Any, bytearray, int, int, int],
        display_data: tuple[Any, bytearray, int, int, int],
        display_configs: DisplayConfig,
    ) -> None:
        # Initialize renderer (docstring removed)
        self.display_configs = display_configs

        self.img_ptr, self.img_adr, self.img_line, _, _ = img_data
        _, _, _, self.img_width, self.img_height = img_data

        self.buff_ptr, self.buff_adr, self.buff_line, _, _ = buff_data
        _, _, _, self.buff_width, self.buff_height = buff_data

        self.display_ptr, self.display_adr, self.display_line, _, _ = (
            display_data
        )
        _, _, _, self.display_width, self.display_height = display_data

        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)
        self.display_array = np.frombuffer(self.display_adr, dtype=np.uint8)

        self.img_3d = self.img_array.reshape(
                                    self.img_height,
                                    self.img_width,
                                    4
                                )
        self.buff_3d = self.buff_array.reshape(
                                    self.buff_height,
                                    self.buff_width,
                                    4
                                )

        self.display_3d = self.display_array.reshape(
                                    self.display_height,
                                    self.display_width,
                                    4
                                )

        self.spritesheet = Spritesheet(self.img_3d)
        self.h_wall, self.h_wall_height, self.h_wall_width = tileset(
            self.display_configs.horizontal_wall_x,
            self.display_configs.horizontal_wall_y,
            self.spritesheet
        )

        self.v_wall, self.v_wall_height, self.v_wall_width = tileset(
            self.display_configs.vertical_wall_x,
            self.display_configs.vertical_wall_y,
            self.spritesheet
        )

        self.b_wall, self.b_wall_height, self.b_wall_width = tileset(
            self.display_configs.bottom_wall_x,
            self.display_configs.bottom_wall_y,
            self.spritesheet
        )

        self.sv_wall, self.sv_wall_height, self.sv_wall_width = tileset(
            self.display_configs.side_v_wall_x,
            self.display_configs.side_v_wall_y,
            self.spritesheet
        )

        self.h_joint, self.h_joint_height, self.h_joint_width = tileset(
            self.display_configs.horizontal_joint_x,
            self.display_configs.horizontal_joint_y,
            self.spritesheet
        )

        self.empty_joint, self.empty_joint_height, self.empty_joint_width = (
            tileset(
                self.display_configs.empty_joint_x,
                self.display_configs.empty_joint_y,
                self.spritesheet
            )
        )

        self.dude, self.dude_height, self.dude_width = tileset(
            self.display_configs.dude_x,
            self.display_configs.dude_y,
            self.spritesheet
        )
        self.money, self.money_height, self.money_width = tileset(
            self.display_configs.money_x,
            self.display_configs.money_y,
            self.spritesheet
        )

        # Scale wall sprites x4 thickness
        self.h_wall = scale_pixel(self.h_wall, 4)
        self.h_wall_height, self.h_wall_width, _ = self.h_wall.shape

        self.v_wall = scale_pixel(self.v_wall, 4)
        self.v_wall_height, self.v_wall_width, _ = self.v_wall.shape

        self.b_wall = scale_pixel(self.b_wall, 4)
        self.b_wall_height, self.b_wall_width, _ = self.b_wall.shape

        self.sv_wall = scale_pixel(self.sv_wall, 4)
        self.sv_wall_height, self.sv_wall_width, _ = self.sv_wall.shape

        self.h_joint = scale_pixel(self.h_joint, 4)
        self.h_joint_height, self.h_joint_width, _ = self.h_joint.shape

        self.empty_joint = scale_pixel(self.empty_joint, 4)
        self.empty_joint_height, self.empty_joint_width, _ = self.empty_joint.shape

        self.dude = scale_pixel(self.dude, 2)
        self.dude_height, self.dude_width, _ = self.dude.shape

        self.money = scale_pixel(self.money, 2)
        self.money_height, self.money_width, _ = self.money.shape

        self.maze_hex: list[list[str]] = []
        self.path: list[tuple[int, int]] = []

        self.theme_cache: dict[str, dict[str, Any]] = {}
        self.fcolors = floor_colors
        self.wcolors = wall_colors
        self.bcolors = background_colors
        self.wcolors_keys = list(self.wcolors.keys())

        # Actual RGBA pixel values in the tileset wall sprites
        WALL_PRIMARY   = [66,  40,  53, 255]
        WALL_SHADOW    = [28,  17,  23, 255]
        WALL_HIGHLIGHT = [117, 103,  96, 255]

        for theme in self.wcolors_keys:
            w1, w2, w3 = self.wcolors[theme]
            f1, f2, f3 = self.fcolors[theme]
            bcolor = self.bcolors[theme]

            t_hw = self.h_wall.copy()
            t_vw = self.v_wall.copy()
            t_svw = self.sv_wall.copy()
            t_bw = self.b_wall.copy()
            t_hj = self.h_joint.copy()
            t_ej = self.empty_joint.copy()

            for sprite in [t_hw, t_vw, t_svw, t_bw, t_hj, t_ej]:
                recolor_pixel(sprite, WALL_PRIMARY,   w1)
                recolor_pixel(sprite, WALL_SHADOW,    w2)
                recolor_pixel(sprite, WALL_HIGHLIGHT, w3)

            self.theme_cache[theme] = {
                "h_wall": t_hw,
                "v_wall": t_vw,
                "b_wall": t_bw,
                "sv_wall": t_svw,
                "hj_wall": t_hj,
                "ej_wall": t_ej,
                "f1": f1,
                "f2": f2,
                "f3": f3,
                "bcolor": bcolor,
            }

        self.active_theme: dict[str, Any] = self.theme_cache["default_theme"]
        self.h_wall, self.v_wall, self.b_wall = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"]
        )
        self.sv_wall, self.h_joint, self.empty_joint = (
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
        )
        self.fcolor1, self.fcolor2, self.fcolor3, self.bcolor = (
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"]
        )

        self.camera_x, self.camera_y = (0, 0)
        self.speed = 20

    def blit(self, y_coords: tuple[int, int], x_coords: tuple[int, int], wall: np.ndarray) -> None:
        # Copy pixel data into the rendering buffer
        start_x, end_x = x_coords
        start_y, end_y = y_coords

        self.buff_3d[start_y:end_y, start_x:end_x] = wall

    def floor(self) -> None:
        # Render floor
        dest_y: int = 0
        for y in range(len(self.maze_hex)):
            dest_x: int = 0
            for x in range(len(self.maze_hex[0])):
                hex_value: str = self.maze_hex[y][x]
                if (hex_value == "F"):
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor2
                    )
                else:
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor1
                    )
                dest_x = dest_x + self.display_configs.cell_width
            dest_y = dest_y + self.display_configs.cell_height

    def cell(self) -> None:
        # Render walls and joints
        dest_y = 0
        for y in range(len(self.maze_hex)):
            dest_x = 0
            for x in range(len(self.maze_hex[0])):
                hex_value = int(self.maze_hex[y][x], 16)

                if (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x, dest_x + self.v_wall_width),
                        self.v_wall
                    )

                if (hex_value & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_wall_height),
                        (dest_x + self.v_wall_width,
                         dest_x + self.v_wall_width + self.h_wall_width),
                        self.h_wall
                    )

                if (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint
                    )

                if not (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.empty_joint_height),
                        (dest_x, dest_x + self.empty_joint_width),
                        self.empty_joint
                    )

                if (x == len(self.maze_hex[0]) - 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x + self.v_wall_width + self.h_wall_width,
                         dest_x + self.v_wall_width * 2 + self.h_wall_width),
                        self.v_wall
                    )

                if (y == len(self.maze_hex) - 1):
                    # Draw bottom walls
                    self.blit(
                        (dest_y + self.sv_wall_height - self.h_joint_height,
                         dest_y + self.sv_wall_height + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint
                    )

                    self.blit(
                        (dest_y + self.sv_wall_height - self.b_wall_height,
                         dest_y + self.sv_wall_height + self.b_wall_height),
                        (dest_x + self.v_wall_width,
                         dest_x + self.v_wall_width + self.b_wall_width),
                        self.b_wall
                    )

                    if (x == len(self.maze_hex[0]) - 1):
                        self.blit(
                            (dest_y, dest_y + self.sv_wall_height),
                            (dest_x + self.v_wall_width + self.h_wall_width,
                             dest_x + self.v_wall_width*2 + self.h_wall_width),
                            self.sv_wall
                        )

                dest_x = dest_x + self.v_wall_width + self.h_wall_width
            dest_y = dest_y + self.v_wall_height

    def entry_and_exit(self) -> None:
        # Draw entry and exit sprites
        entry_x, entry_y = self.display_configs.entry_point
        exit_x, exit_y = self.display_configs.exit_point

        dest_entry_x = entry_x * self.display_configs.cell_width
        dest_entry_y = entry_y * self.display_configs.cell_height

        dest_exit_x = exit_x * self.display_configs.cell_width
        dest_exit_y = exit_y * self.display_configs.cell_height

        self.blit(
            (dest_entry_y + 10, dest_entry_y + self.dude_height + 10),
            (dest_entry_x + 12, dest_entry_x + self.dude_width + 12),
            self.dude
        )

        self.blit(
            (dest_exit_y + 10, dest_exit_y + self.money_height + 10),
            (dest_exit_x + 12, dest_exit_x + self.money_width + 12),
            self.money
        )

    def render_path(self) -> None:
        # Render solution path
        for coord in self.path:
            x, y = coord

            dest_x = x * self.display_configs.cell_width
            dest_y = y * self.display_configs.cell_height

            self.blit(
                (dest_y, dest_y + self.display_configs.cell_height),
                (dest_x, dest_x + self.display_configs.cell_width),
                self.fcolor3
            )
        self.cell()

    def maze(self) -> None:
        # Render full maze
        self.floor()
        self.cell()

    def change_wall_color(self) -> None:
        # Cycle theme
        current_idx = self.wcolors_keys.index(
            next(k for k, v in self.theme_cache.items()
                 if v is self.active_theme)
        )
        key = self.wcolors_keys[(current_idx + 1) % len(self.wcolors_keys)]
        self.active_theme = self.theme_cache[key]

        self.h_wall, self.v_wall, self.b_wall = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"]
        )
        self.sv_wall, self.h_joint, self.empty_joint = (
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
        )
        self.fcolor1, self.fcolor2, self.fcolor3, self.bcolor = (
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"]
        )

    def present(self) -> None:
        # Present buffer to display
        self.display_3d[:] = self.bcolor

        visible_h = min(self.buff_height, self.display_height)
        visible_w = min(self.buff_width, self.display_width)

        offset_x = max(0, (self.display_width - self.buff_width) // 2)
        offset_y = max(0, (self.display_height - self.buff_height) // 2)

        self.camera_x = max(0, min(
                self.camera_x, self.buff_width - self.display_width
            )
        )
        self.camera_y = max(0, min(
                self.camera_y, self.buff_height - self.display_height
            )
        )

        self.display_3d[
            offset_y:offset_y + visible_h,
            offset_x:offset_x + visible_w
        ] = self.buff_3d[
            self.camera_y:self.camera_y + visible_h,
            self.camera_x:self.camera_x + visible_w,
        ]


# Compatibility wrapper used by the top-level script. The original
# project expected a `MazeRenderer` class to create and run an MLX
# window. Implement a minimal stub so importing `MazeRenderer`
# succeeds even when the full MLX GUI isn't available.
class MazeRenderer:
    # Minimal MLX renderer (docstrings removed)
    def __init__(self, maze_matrix, width, height, isolated=None):
        from mlx import Mlx
        import numpy as _np
        self.maze = maze_matrix
        self.width = width
        self.height = height
        self.cell_w = 16
        self.cell_h = 16
        self.wall_thickness = 5

        self.win_w = self.width * self.cell_w
        self.win_h = self.height * self.cell_h

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "a_maze_ing"
        )

        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        self.img_adr, self.bits_per_pixel, self.size_line, _fmt = self.mlx.mlx_get_data_addr(self.img_ptr)

        arr = _np.frombuffer(self.img_adr, dtype=_np.uint8)
        bytes_per_pixel = max(1, self.bits_per_pixel // 8)
        self.img_h = int(len(arr) // self.size_line)
        self.frame = arr.reshape(self.img_h, self.size_line)[:, : self.win_w * bytes_per_pixel]
        self.frame = self.frame.reshape(self.img_h, self.win_w, bytes_per_pixel)

        self._regen_cb = None

        # store isolated cell coordinates (set of (x,y)) to highlight
        try:
            self.isolated = set(isolated) if isolated is not None else set()
        except Exception:
            self.isolated = set()

        # Try to load an external tileset image (tileset.png) to draw sprites.
        # If PIL is unavailable or the file not present, fall back to simple rects.
        self.tileset = None
        try:
            from PIL import Image
            import os
            tileset_path = os.path.join(os.getcwd(), "tileset.png")
            if os.path.exists(tileset_path):
                img = Image.open(tileset_path).convert("RGBA")
                t_arr = _np.array(img, dtype=_np.uint8)
                # Ensure shape (H, W, 4)
                if t_arr.ndim == 3 and t_arr.shape[2] >= 3:
                    # If alpha missing, add opaque channel
                    if t_arr.shape[2] == 3:
                        alpha = _np.full((t_arr.shape[0], t_arr.shape[1], 1), 255, dtype=_np.uint8)
                        t_arr = _np.concatenate([t_arr, alpha], axis=2)
                    self.tileset = t_arr
                    # Split into tile grid of cell size if possible
                    th, tw, _ = self.tileset.shape
                    tiles_x = max(1, tw // self.cell_w)
                    tiles_y = max(1, th // self.cell_h)
                    self._tiles = []
                    for ty in range(tiles_y):
                        row = []
                        for tx in range(tiles_x):
                            x0 = tx * self.cell_w
                            y0 = ty * self.cell_h
                            row.append(self.tileset[y0:y0 + self.cell_h, x0:x0 + self.cell_w].copy())
                        self._tiles.append(row)
        except Exception:
            self.tileset = None

        # Optional external wall texture: if a file named wall_texture.png
        # exists in the cwd, load and resize it to the cell size so it can
        # be blitted on walls instead of plain rectangles.
        self.wall_texture = None
        try:
            import os
            wt_path = os.path.join(os.getcwd(), "wall_texture.png")
            if os.path.exists(wt_path):
                from PIL import Image
                wt_img = Image.open(wt_path).convert("RGBA")
                # resize to exactly one cell
                if (wt_img.width, wt_img.height) != (self.cell_w, self.cell_h):
                    wt_img = wt_img.resize((self.cell_w, self.cell_h), Image.BILINEAR)
                wt_arr = _np.array(wt_img, dtype=_np.uint8)
                if wt_arr.ndim == 3 and wt_arr.shape[2] == 3:
                    alpha = _np.full((wt_arr.shape[0], wt_arr.shape[1], 1), 255, dtype=_np.uint8)
                    wt_arr = _np.concatenate([wt_arr, alpha], axis=2)
                self.wall_texture = wt_arr
                print("[renderer] wall_texture.png found and loaded")
        except Exception:
            self.wall_texture = None
            print("[renderer] wall_texture not available (PIL missing or load failed)")

    def set_regen_callback(self, cb):
        self._regen_cb = cb

    def _fill_rect(self, x0, y0, w, h, color):
        # color is (r,g,b,a) 0-255
        r, g, b, a = color
        # frame uses BGRA or RGBA depending on MLX; try RGBA ordering
        try:
            self.frame[y0 : y0 + h, x0 : x0 + w, 0] = r
            self.frame[y0 : y0 + h, x0 : x0 + w, 1] = g
            self.frame[y0 : y0 + h, x0 : x0 + w, 2] = b
            if self.frame.shape[2] > 3:
                self.frame[y0 : y0 + h, x0 : x0 + w, 3] = a
        except Exception:
            pass

    def _blit_sprite(self, x0, y0, sprite, src_box=None):
        """Blit an RGBA sprite (numpy array) into the frame at x0,y0.

        If `src_box` is provided, it should be a tuple (sy, ey, sx, ex)
        describing the source rectangle within `sprite` to copy.
        """
        try:
            s = sprite
            if src_box is not None:
                sy, ey, sx, ex = src_box
                s = sprite[sy:ey, sx:ex]

            h, w, c = s.shape
            if h == 0 or w == 0:
                return

            # destination bounds
            dy0 = max(0, y0)
            dx0 = max(0, x0)
            dy1 = min(self.frame.shape[0], y0 + h)
            dx1 = min(self.frame.shape[1], x0 + w)

            sy0 = dy0 - y0
            sx0 = dx0 - x0
            sy1 = sy0 + (dy1 - dy0)
            sx1 = sx0 + (dx1 - dx0)

            # extract source region and target region
            src = s[sy0:sy1, sx0:sx1]
            dst = self.frame[dy0:dy1, dx0:dx1]

            # Composite src over dst using alpha if present, otherwise copy
            try:
                import numpy as _np
                if src.shape[2] >= 4:
                    # alpha composite
                    src_rgb = src[..., :3].astype(_np.float32)
                    alpha = (src[..., 3:4].astype(_np.float32) / 255.0)
                    dst_rgb = dst[..., :3].astype(_np.float32)
                    out_rgb = (src_rgb * alpha + dst_rgb * (1.0 - alpha)).astype(_np.uint8)
                    dst[..., :3] = out_rgb
                    if dst.shape[2] > 3:
                        dst[..., 3] = src[..., 3]
                else:
                    # direct copy of RGB channels
                    if dst.shape[2] >= 3 and src.shape[2] >= 3:
                        dst[:, :, :3] = src[:, :, :3]
                        if dst.shape[2] > 3 and src.shape[2] > 3:
                            dst[:, :, 3] = src[:, :, 3]
                    else:
                        dst[:] = src[:, :, :dst.shape[2]]
            except Exception:
                try:
                    # fallback: try BGRA ordering
                    if dst.shape[2] >= 3 and src.shape[2] >= 3:
                        dst[:, :, 2] = src[:, :, 0]
                        dst[:, :, 1] = src[:, :, 1]
                        dst[:, :, 0] = src[:, :, 2]
                        if dst.shape[2] > 3 and src.shape[2] > 3:
                            dst[:, :, 3] = src[:, :, 3]
                except Exception:
                    pass
        except Exception:
            pass

    def draw_maze(self):
        # simple palette fallback
        floor = (60, 60, 60, 255)
        wall = (20, 20, 20, 255)

        # clear background
        if self.tileset is None:
            if self.wall_texture is not None:
                # Tile background using provided texture
                for ty in range(self.height):
                    for tx in range(self.width):
                        px = tx * self.cell_w
                        py = ty * self.cell_h
                        self._blit_sprite(px, py, self.wall_texture)
            else:
                self._fill_rect(0, 0, self.win_w, self.win_h, floor)
        else:
            # Tile background by floor tile if available, else fall back to texture or solid
            try:
                floor_tile = self._tiles[0][0]
                for ty in range(self.height):
                    for tx in range(self.width):
                        px = tx * self.cell_w
                        py = ty * self.cell_h
                        self._blit_sprite(px, py, floor_tile)
            except Exception:
                if self.wall_texture is not None:
                    for ty in range(self.height):
                        for tx in range(self.width):
                            px = tx * self.cell_w
                            py = ty * self.cell_h
                            self._blit_sprite(px, py, self.wall_texture)
                else:
                    self._fill_rect(0, 0, self.win_w, self.win_h, floor)

            # (wall_texture is applied during wall drawing)

        for y in range(self.height):
            wt_count = 0
            for x in range(self.width):
                v = int(self.maze[y][x]) if isinstance(self.maze[y][x], int) or (isinstance(self.maze[y][x], str) and self.maze[y][x].isdigit()) else int(self.maze[y][x])
                px = x * self.cell_w
                py = y * self.cell_h

                # Highlight isolated cells (fill with a distinct color)
                if (x, y) in self.isolated:
                    iso_color = (200, 40, 40, 255)
                    if self.tileset is not None:
                        try:
                            iso_tile = self._tiles[0][0]
                            self._blit_sprite(px, py, iso_tile)
                        except Exception:
                            self._fill_rect(px, py, self.cell_w, self.cell_h, iso_color)
                    else:
                        self._fill_rect(px, py, self.cell_w, self.cell_h, iso_color)

                if self.tileset is not None:
                    # choose tile variants if present
                    try:
                        wall_tile = self._tiles[0][1] if len(self._tiles[0]) > 1 else self._tiles[0][0]
                    except Exception:
                        wall_tile = None

                    # Interpret bits as: 1=top, 2=right, 4=bottom, 8=left
                    if v & 1:
                        # top wall: use wall_tile if present, else solid fill
                        if wall_tile is not None:
                            self._blit_sprite(px, py, wall_tile, src_box=(0, self.wall_thickness, 0, self.cell_w))
                        else:
                            self._fill_rect(px, py, self.cell_w, self.wall_thickness, wall)
                    if v & 2:
                        # right wall
                        if wall_tile is not None:
                            self._blit_sprite(px + self.cell_w - self.wall_thickness, py, wall_tile, src_box=(0, self.cell_h, self.cell_w - self.wall_thickness, self.cell_w))
                        else:
                            self._fill_rect(px + self.cell_w - self.wall_thickness, py, self.wall_thickness, self.cell_h, wall)
                    if v & 4:
                        # bottom wall
                        if wall_tile is not None:
                            self._blit_sprite(px, py + self.cell_h - self.wall_thickness, wall_tile, src_box=(self.cell_h - self.wall_thickness, self.cell_h, 0, self.cell_w))
                        else:
                            self._fill_rect(px, py + self.cell_h - self.wall_thickness, self.cell_w, self.wall_thickness, wall)
                    if v & 8:
                        # left wall
                        if wall_tile is not None:
                            self._blit_sprite(px, py, wall_tile, src_box=(0, self.cell_h, 0, self.wall_thickness))
                        else:
                            self._fill_rect(px, py, self.wall_thickness, self.cell_h, wall)
                else:
                    # Interpret bits as: 1=top, 2=right, 4=bottom, 8=left
                    if v & 1:
                        self._fill_rect(px, py, self.cell_w, self.wall_thickness, wall)
                    if v & 2:
                        self._fill_rect(px + self.cell_w - self.wall_thickness, py, self.wall_thickness, self.cell_h, wall)
                    if v & 4:
                        self._fill_rect(px, py + self.cell_h - self.wall_thickness, self.cell_w, self.wall_thickness, wall)
                    if v & 8:
                        self._fill_rect(px, py, self.wall_thickness, self.cell_h, wall)

    def _on_key(self, keycode, param):
        # exit on any key
        try:
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        except Exception:
            pass

    def run(self):
        # draw once and show
        try:
            self.draw_maze()
            self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

            # hook keys to exit
            def _key_cb(k, p):
                self._on_key(k, p)

            self.mlx.mlx_key_hook(self.win_ptr, _key_cb, None)
            # Handle window close (X11 Destroy/ClientMessage). Event 17
            def _close_cb(p):
                try:
                    self.mlx.mlx_loop_exit(self.mlx_ptr)
                except Exception:
                    pass

            # Try both Destroy (17) and ClientMessage (33) for window close
            try:
                self.mlx.mlx_hook(self.win_ptr, 17, 0, _close_cb, None)
            except Exception:
                pass
            try:
                self.mlx.mlx_hook(self.win_ptr, 33, 0, _close_cb, None)
            except Exception:
                pass

            self.mlx.mlx_loop(self.mlx_ptr)
        except Exception as e:
            print("MLX renderer failed to start:", e)