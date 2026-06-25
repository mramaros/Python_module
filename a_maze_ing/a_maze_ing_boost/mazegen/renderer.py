#!/usr/bin/env python3
# ########################################################################### #
#   renderer.py                                          :+:      :+:    :+:  #
# ########################################################################### #

import os
import sys
from .generate_cellule.class_cell import Cell
from mlx import Mlx
from .generate_cellule.generate_cellule import get_cell

HAS_PIL = False

user_site = "/home/mramaros/.local/lib/python3.13/site-packages"
if user_site not in sys.path:
    sys.path.insert(0, user_site)

try:
    from PIL import Image
    HAS_PIL = True
    print("✅ PIL chargé avec succès")
except ImportError as e:
    print(f"⚠️  Erreur import PIL: {e}")
    print("   Utilisation des textures générées")
    HAS_PIL = False


class maze_mlx:
    """Wrapper minimal autour de la librairie `Mlx` pour dessiner le labyrinthe."""

    def __init__(self, COLS: int, ROWS: int, CELL_SIZE: int = 20, OUTLINE_THICKNESS: int = 2) -> None:
        self.COLS = COLS
        self.ROWS = ROWS
        self.current_env = "normal"
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(
            self.mlx_ptr, COLS + 30, ROWS + 80, "A-Maze-ing"
        )
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, COLS, ROWS)

        self.data, self.bpp, self.sl, self.fmt = self.mlx.mlx_get_data_addr(
            self.img
        )

        self.wall_textures = self._load_or_create_textures()
        self.fallback_color = 0xFFFFFFFF
        self.clear_img()

    def change_environment(self, env_name: str):
        """Change dynamiquement l'environnement et recharge les textures."""
        self.current_env = env_name
        self.wall_textures = self._load_or_create_textures()

    def _load_or_create_textures(self):
        textures = {}
        print(f"📂 Recherche des images dans: referance_a_maze_ing/ pour {self.current_env.upper()}")
        if HAS_PIL:
            textures = self._load_textures_with_pil(self.current_env)
        else:
            print("⚠️  PIL non disponible, utilisation des textures générées")
            textures = self._create_textures()

        if textures.get("horizontal") is None:
            textures["horizontal"] = self._create_simple_texture(20, 6, 0xFFFFFFFF)
        if textures.get("vertical") is None:
            textures["vertical"] = self._create_simple_texture(6, 20, 0xFFFFFFFF)
        if textures.get("sol") is None:
            textures["sol"] = self._create_simple_texture(20, 20, 0xFF443322)
        return textures

    def _load_textures_with_pil(self, env_name="normal"):
        textures = {}
        base_path = "referance_a_maze_ing/"
        if not os.path.exists(base_path):
            print(f"❌ Dossier non trouvé: {base_path}")
            return textures

        noms_fichiers = {
            "normal": ("mur_horizontal", "mur_vertical", "sol_par_cell"),
            "sable": ("mur_horizontal_sable", "mur_vretical_sable", "sol_par_cell_sable"),
            "donjon": ("mur_horizontal_donjon", "mur_vertical_donjon", "sol_par_cell_donjon"),
            "lave": ("mur_horizontal_lave", "mur_vertical_lave", "sol_par_cell_lave"),
            "glace": ("mur_horizontal_glace", "mur_vertical_glace", "sol_par_cell_glace")
        }
        
        h_name, v_name, s_name = noms_fichiers.get(env_name, noms_fichiers["normal"])

        self._load_single_texture(textures, "horizontal", base_path, h_name)
        self._load_single_texture(textures, "vertical", base_path, v_name)
        self._load_single_texture(textures, "sol", base_path, s_name)

        return textures

    def _load_single_texture(self, textures, key, base_path, base_name):
        extensions = [".png", ".jpg", ".jpeg"]
        loaded = False
        for ext in extensions:
            path = os.path.join(base_path, f"{base_name}{ext}")
            if os.path.exists(path):
                try:
                    img = Image.open(path).convert("RGBA")
                    pixels = []
                    width, height = img.size
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = img.getpixel((x, y))
                            pixels.append((a << 24) | (r << 16) | (g << 8) | b)
                    textures[key] = {"pixels": pixels, "width": width, "height": height}
                    print(f"  ✅ Texture {key} chargée: {path}")
                    loaded = True
                    break
                except Exception as e:
                    print(f"  ❌ Erreur sur {path}: {e}")
                    
        if not loaded:
            print(f"  ⚠️  Texture introuvable pour : {base_name}")

    def _create_textures(self):
        textures = {}
        width, height = 20, 8
        pixels = []
        for y in range(height):
            for x in range(width):
                color = 0xFFFFFFFF if (y != 0 and y != 7) else 0xFFBBBBBB
                pixels.append(color)
        textures["horizontal"] = {"pixels": pixels, "width": width, "height": height}

        width, height = 8, 20
        pixels = []
        for y in range(height):
            for x in range(width):
                color = 0xFFFFFFFF if (x != 0 and x != 7) else 0xFFBBBBBB
                pixels.append(color)
        textures["vertical"] = {"pixels": pixels, "width": width, "height": height}

        textures["sol"] = {"pixels": [0xFF443322] * 400, "width": 20, "height": 20}
        return textures

    def _create_simple_texture(self, width, height, color):
        return {"pixels": [color] * (width * height), "width": width, "height": height}

    def put_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            offset = y * self.sl + x * (self.bpp // 8)
            self.data[offset : offset + 4] = color.to_bytes(4, "little")

    def draw_line_h(self, x0: int, y0: int, length: int, color: int, thickness=6) -> None:
        for t in range(thickness):
            for dx in range(length):
                self.put_pixel(x0 + dx, y0 + t, color)

    def draw_line_v(self, x0: int, y0: int, length: int, color: int, thickness=3) -> None:
        for t in range(thickness):
            for dy in range(length):
                self.put_pixel(x0 + t, y0 + dy, color)

    def _get_pixel_from_texture(self, texture, x, y):
        if texture is None: return self.fallback_color
        pixels = texture["pixels"]
        tex_x = x % texture["width"]
        tex_y = y % texture["height"]
        return pixels[tex_y * texture["width"] + tex_x]

    def _draw_textured_ground(self, x0, y0, size_to_draw, texture):
        if texture is None: return
        tex_w, tex_h, pixels = texture["width"], texture["height"], texture["pixels"]
        for dy in range(size_to_draw):
            for dx in range(size_to_draw):
                tex_x = min(int((dx / size_to_draw) * tex_w), tex_w - 1)
                tex_y = min(int((dy / size_to_draw) * tex_h), tex_h - 1)
                self.put_pixel(x0 + dx, y0 + dy, pixels[tex_y * tex_w + tex_x])

    def _draw_textured_horizontal_wall(self, x0, y0, length, texture, cell_x, cell_y, cell_size, thickness):
        if texture is None:
            self.draw_line_h(x0, y0, length, self.fallback_color, thickness)
            return
        for dy in range(thickness):
            for dx in range(length):
                global_x = (cell_x * cell_size) + dx
                self.put_pixel(x0 + dx, y0 + dy, self._get_pixel_from_texture(texture, global_x, dy))

    def _draw_textured_vertical_wall(self, x0, y0, length, texture, cell_x, cell_y, cell_size, thickness):
        if texture is None:
            self.draw_line_v(x0, y0, length, self.fallback_color, thickness)
            return
        for dx in range(thickness):
            for dy in range(length):
                global_y = (cell_y * cell_size) + dy
                self.put_pixel(x0 + dx, y0 + dy, self._get_pixel_from_texture(texture, dx, global_y))

    def fill_all_ground(self, WIDTH: int, HEIGHT: int):
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        if not self.wall_textures.get("sol"):
            return
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self._draw_textured_ground(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    self.wall_textures["sol"]
                )

    def render_with_textures(self, all_cell: list[Cell], WIDTH: int, HEIGHT: int, CELL_SIZE: int, OUTLINE_THICKNESS: int) -> None:
        if self.wall_textures.get("sol"):
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    x0, y0 = x * CELL_SIZE, y * CELL_SIZE
                    self._draw_textured_ground(
                        x0, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["sol"]
                    )

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cell = get_cell(all_cell, x, y, WIDTH)
                x0, y0 = x * CELL_SIZE, y * CELL_SIZE

                if cell.wall[0]:
                    self._draw_textured_horizontal_wall(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["horizontal"], x, y, CELL_SIZE, OUTLINE_THICKNESS)
                if cell.wall[2]:
                    self._draw_textured_horizontal_wall(x0, y0 + CELL_SIZE, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["horizontal"], x, y, CELL_SIZE, OUTLINE_THICKNESS)
                if cell.wall[3]:
                    self._draw_textured_vertical_wall(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["vertical"], x, y, CELL_SIZE, OUTLINE_THICKNESS)
                if cell.wall[1]:
                    self._draw_textured_vertical_wall(x0 + CELL_SIZE, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["vertical"], x, y, CELL_SIZE, OUTLINE_THICKNESS)

        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 15, 15)

    def draw_cell_with_texture(self, cell: Cell, WIDTH: int, HEIGHT: int, CELL_SIZE: int, OUTLINE_THICKNESS: int, all_cell: list[Cell]) -> None:
        x0, y0 = cell.x * CELL_SIZE, cell.y * CELL_SIZE

        if cell.wall[0]:
            self._draw_textured_horizontal_wall(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["horizontal"], cell.x, cell.y, CELL_SIZE, OUTLINE_THICKNESS)
        if cell.wall[2]:
            self._draw_textured_horizontal_wall(x0, y0 + CELL_SIZE, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["horizontal"], cell.x, cell.y, CELL_SIZE, OUTLINE_THICKNESS)
        if cell.wall[3]:
            self._draw_textured_vertical_wall(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["vertical"], cell.x, cell.y, CELL_SIZE, OUTLINE_THICKNESS)
        if cell.wall[1]:
            self._draw_textured_vertical_wall(x0 + CELL_SIZE, y0, CELL_SIZE + OUTLINE_THICKNESS, self.wall_textures["vertical"], cell.x, cell.y, CELL_SIZE, OUTLINE_THICKNESS)

    def color_entry_and_exit(self, ENTRY_X: int, ENTRY_Y: int, EXIT_X: int, EXIT_Y: int):
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        for x in range(ENTRY_X, ENTRY_X + CELL_SIZE - OUTLINE_THICKNESS):
            for y in range(ENTRY_Y, ENTRY_Y + CELL_SIZE - OUTLINE_THICKNESS):
                self.put_pixel(x, y, 0xFF00FF00)
        for x in range(EXIT_X, EXIT_X + CELL_SIZE - OUTLINE_THICKNESS):
            for y in range(EXIT_Y, EXIT_Y + CELL_SIZE - OUTLINE_THICKNESS):
                self.put_pixel(x, y, 0xFF2F4F4F)

    # ✅ LA CORRECTION SE TROUVE ICI
    def color_content_solver(self, all_cell: list[Cell], WIDTH: int, his_x: int, his_y: int, index: int, solver: list[tuple[int, int]], color: int):
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        
        # 1. Calcul du vrai centre dans le couloir vide (offset depuis le mur)
        # Si CELL_SIZE = 32 et OUTLINE_THICKNESS = 12 : l'offset sera 12 + (32 - 12) // 2 = 22.
        offset = OUTLINE_THICKNESS + (CELL_SIZE - OUTLINE_THICKNESS) // 2
        
        center_x = his_x * CELL_SIZE + offset
        center_y = his_y * CELL_SIZE + offset
        
        # 2. Adaptation de l'épaisseur du trait au couloir (environ 1/3 de l'espace dispo)
        path_thickness = max(1, (CELL_SIZE - OUTLINE_THICKNESS) // 3)
        cm = path_thickness // 2

        # Dessin du point central
        for dx in range(-cm, cm + 1):
            for dy in range(-cm, cm + 1):
                self.put_pixel(center_x + dx, center_y + dy, color)

        # Tracé de la ligne vers la cellule suivante
        if index < len(solver) - 1:
            next_x, next_y = solver[index + 1]
            next_center_x = next_x * CELL_SIZE + offset
            next_center_y = next_y * CELL_SIZE + offset

            if center_x == next_center_x:
                y1 = min(center_y, next_center_y)
                y2 = max(center_y, next_center_y)
                for x in range(center_x - cm, center_x + cm + 1):
                    for y in range(y1, y2 + 1):
                        self.put_pixel(x, y, color)
            else:
                x1 = min(center_x, next_center_x)
                x2 = max(center_x, next_center_x)
                for x in range(x1, x2 + 1):
                    for y in range(center_y - cm, center_y + cm + 1):
                        self.put_pixel(x, y, color)

    def color_isoler(self, isoler: set, cell_iso: tuple[int, int], color: int):
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        
        if not hasattr(self, '_full_isoler_set'):
            self._full_isoler_set = set(isoler) | {cell_iso}
            
        iso_x, iso_y = cell_iso
        x0 = iso_x * CELL_SIZE
        y0 = iso_y * CELL_SIZE
        
        for x in range(x0 + OUTLINE_THICKNESS, x0 + CELL_SIZE):
            for y in range(y0 + OUTLINE_THICKNESS, y0 + CELL_SIZE):
                self.put_pixel(x, y, color)

        if (iso_x + 1, iso_y) in self._full_isoler_set: 
            for x in range(x0 + CELL_SIZE, x0 + CELL_SIZE + OUTLINE_THICKNESS):
                for y in range(y0, y0 + CELL_SIZE + OUTLINE_THICKNESS):
                    self.put_pixel(x, y, color)

        if (iso_x - 1, iso_y) in self._full_isoler_set: 
            for x in range(x0, x0 + OUTLINE_THICKNESS):
                for y in range(y0, y0 + CELL_SIZE + OUTLINE_THICKNESS):
                    self.put_pixel(x, y, color)

        if (iso_x, iso_y + 1) in self._full_isoler_set: 
            for x in range(x0, x0 + CELL_SIZE + OUTLINE_THICKNESS):
                for y in range(y0 + CELL_SIZE, y0 + CELL_SIZE + OUTLINE_THICKNESS):
                    self.put_pixel(x, y, color)

        if (iso_x, iso_y - 1) in self._full_isoler_set: 
            for x in range(x0, x0 + CELL_SIZE + OUTLINE_THICKNESS):
                for y in range(y0, y0 + OUTLINE_THICKNESS):
                    self.put_pixel(x, y, color)

    def clear_img(self):
        black = 0xFF000000
        for y in range(self.ROWS):
            for x in range(self.COLS):
                self.put_pixel(x, y, black)

    def render(self, all_cell: list[Cell], color: int) -> None:
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        for c in all_cell:
            x0 = c.x * CELL_SIZE
            y0 = c.y * CELL_SIZE
            if c.wall[0]:
                self.draw_line_h(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
            if c.wall[1]:
                self.draw_line_v(x0 + CELL_SIZE, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
            if c.wall[2]:
                self.draw_line_h(x0, y0 + CELL_SIZE, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
            if c.wall[3]:
                self.draw_line_v(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 15, 15)

    def draw_cell(self, cell: Cell, color: int) -> None:
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS
        x0 = cell.x * CELL_SIZE
        y0 = cell.y * CELL_SIZE
        if cell.wall[0]:
            self.draw_line_h(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
        if cell.wall[1]:
            self.draw_line_v(x0 + CELL_SIZE, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
        if cell.wall[2]:
            self.draw_line_h(x0, y0 + CELL_SIZE, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
        if cell.wall[3]:
            self.draw_line_v(x0, y0, CELL_SIZE + OUTLINE_THICKNESS, color, OUTLINE_THICKNESS)
