#!/usr/bin/env python3
# ########################################################################### #
#   renderer.py                                          :+:      :+:    :+:  #
# ########################################################################### #

import os
import sys
from .generate_cellule.class_cell import Cell
from mlx import Mlx
from .generate_cellule.generate_cellule import get_cell

# === FORCER L'IMPORT DE PIL ===
HAS_PIL = False

# Ajouter explicitement le chemin utilisateur
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

    def __init__(self, COLS: int, ROWS: int) -> None:
        """Initialise une fenêtre et un buffer image pour le rendu."""
        self.COLS = COLS
        self.ROWS = ROWS
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(
            self.mlx_ptr, COLS + 30, ROWS + 80, "A-Maze-ing"
        )
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, COLS, ROWS)

        self.data, self.bpp, self.sl, self.fmt = self.mlx.mlx_get_data_addr(
            self.img
        )

        # Charger ou créer les textures
        self.wall_textures = self._load_or_create_textures()
        self.fallback_color = 0xFFFFFFFF  # Blanc

    def _load_or_create_textures(self):
        """Charge les images depuis les fichiers ou crée des textures par défaut."""
        textures = {}

        print(f"📂 Recherche des images dans: referance_a_maze_ing/")

        # Essayer de charger les images
        if HAS_PIL:
            print("🖼️  Chargement des textures avec PIL...")
            textures = self._load_textures_with_pil()
        else:
            print("⚠️  PIL non disponible, utilisation des textures générées")
            textures = self._create_textures()

        # Si le chargement a échoué, utiliser les textures par défaut
        if textures.get("horizontal") is None:
            textures["horizontal"] = self._create_simple_texture(
                20, 6, 0xFFFFFFFF
            )
            print("⚠️  Utilisation de la texture horizontale par défaut")

        if textures.get("vertical") is None:
            textures["vertical"] = self._create_simple_texture(
                6, 20, 0xFFFFFFFF
            )
            print("⚠️  Utilisation de la texture verticale par défaut")

        return textures

    def _load_textures_with_pil(self):
        """Charge les textures avec PIL."""
        textures = {}

        # Chemin vers les images
        base_path = "referance_a_maze_ing/"

        # Vérifier si le dossier existe
        if not os.path.exists(base_path):
            print(f"❌ Dossier non trouvé: {base_path}")
            return textures

        # Lister les fichiers dans le dossier
        print(f"📁 Contenu de {base_path}:")
        try:
            for f in os.listdir(base_path):
                print(f"   - {f}")
        except:
            print("   (impossible de lister le dossier)")

        # Chercher les images dans différents formats
        extensions = [".png", ".xpm", ".jpg", ".jpeg"]

        # Charger l'image horizontale
        for ext in extensions:
            path = os.path.join(base_path, f"mur_horizontal{ext}")
            if os.path.exists(path):
                try:
                    print(f"📂 Chargement: {path}")
                    img = Image.open(path)
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")

                    # Extraire les pixels
                    pixels = []
                    width, height = img.size
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = img.getpixel((x, y))
                            color = (a << 24) | (r << 16) | (g << 8) | b
                            pixels.append(color)

                    textures["horizontal"] = {
                        "pixels": pixels,
                        "width": width,
                        "height": height,
                    }
                    print(
                        f"✅ Texture horizontale chargée: {path} ({width}x{height})"
                    )
                    break
                except Exception as e:
                    print(f"❌ Erreur chargement {path}: {e}")
                    textures["horizontal"] = None

        # Charger l'image verticale
        for ext in extensions:
            path = os.path.join(base_path, f"mur_vertical{ext}")
            if os.path.exists(path):
                try:
                    print(f"📂 Chargement: {path}")
                    img = Image.open(path)
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")

                    pixels = []
                    width, height = img.size
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = img.getpixel((x, y))
                            color = (a << 24) | (r << 16) | (g << 8) | b
                            pixels.append(color)

                    textures["vertical"] = {
                        "pixels": pixels,
                        "width": width,
                        "height": height,
                    }
                    print(
                        f"✅ Texture verticale chargée: {path} ({width}x{height})"
                    )
                    break
                except Exception as e:
                    print(f"❌ Erreur chargement {path}: {e}")
                    textures["vertical"] = None

        return textures

    def _create_textures(self):
        """Crée des textures en mémoire avec un motif de briques réaliste."""
        textures = {}

        # === Texture HORIZONTALE (mur) ===
        width = 20
        height = 8
        pixels = []
        for y in range(height):
            for x in range(width):
                if y < 4:  # Moitié supérieure
                    if (x // 10) % 2 == 0:
                        if y == 0 or y == 3:
                            color = 0xFFDDDDDD
                        else:
                            color = 0xFFFFFFFF
                    else:
                        if y == 0 or y == 3:
                            color = 0xFFBBBBBB
                        else:
                            color = 0xFFCCCCCC
                else:  # Moitié inférieure
                    if (x // 10) % 2 == 0:
                        if y == 4 or y == 7:
                            color = 0xFFBBBBBB
                        else:
                            color = 0xFFCCCCCC
                    else:
                        if y == 4 or y == 7:
                            color = 0xFFDDDDDD
                        else:
                            color = 0xFFFFFFFF
                pixels.append(color)

        textures["horizontal"] = {
            "pixels": pixels,
            "width": width,
            "height": height,
        }

        # === Texture VERTICALE (mur) ===
        width = 8
        height = 20
        pixels = []
        for y in range(height):
            for x in range(width):
                if x < 4:  # Moitié gauche
                    if (y // 10) % 2 == 0:
                        if x == 0 or x == 3:
                            color = 0xFFDDDDDD
                        else:
                            color = 0xFFFFFFFF
                    else:
                        if x == 0 or x == 3:
                            color = 0xFFBBBBBB
                        else:
                            color = 0xFFCCCCCC
                else:  # Moitié droite
                    if (y // 10) % 2 == 0:
                        if x == 4 or x == 7:
                            color = 0xFFBBBBBB
                        else:
                            color = 0xFFCCCCCC
                    else:
                        if x == 4 or x == 7:
                            color = 0xFFDDDDDD
                        else:
                            color = 0xFFFFFFFF
                pixels.append(color)

        textures["vertical"] = {
            "pixels": pixels,
            "width": width,
            "height": height,
        }

        print("✅ Textures générées en mémoire (motif brique réaliste)")
        return textures

    def _create_simple_texture(self, width, height, color):
        """Crée une texture unie."""
        pixels = [color] * (width * height)
        return {"pixels": pixels, "width": width, "height": height}

    def put_pixel(self, x: int, y: int, color: int) -> None:
        """Place un pixel dans le buffer image."""
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            offset = y * self.sl + x * (self.bpp // 8)
            self.data[offset : offset + 4] = color.to_bytes(4, "little")

    def draw_line_h(
        self, x0: int, y0: int, length: int, color: int, thickness=6
    ) -> None:
        """Dessine une ligne horizontale remplie."""
        for t in range(thickness):
            for dx in range(length):
                self.put_pixel(x0 + dx, y0 + t, color)

    def draw_line_v(
        self, x0: int, y0: int, length: int, color: int, thickness=3
    ) -> None:
        """Dessine une ligne verticale remplie."""
        for t in range(thickness):
            for dy in range(length):
                self.put_pixel(x0 + t, y0 + dy, color)

    def _get_pixel_from_texture(self, texture, x, y):
        """Récupère un pixel d'une texture avec wrapping."""
        if texture is None:
            return self.fallback_color

        pixels = texture["pixels"]
        width = texture["width"]
        height = texture["height"]

        tex_x = x % width
        tex_y = y % height
        index = tex_y * width + tex_x

        if index < len(pixels):
            return pixels[index]
        return self.fallback_color

    def _draw_textured_horizontal_wall(
        self, x0, y0, length, texture, cell_x, cell_y, cell_size, thickness
    ):
        """Dessine un mur horizontal avec texture continue."""
        if texture is None:
            self.draw_line_h(x0, y0, length, self.fallback_color, thickness)
            return

        for dy in range(thickness):
            for dx in range(length):
                global_x = (cell_x * cell_size) + dx
                color = self._get_pixel_from_texture(texture, global_x, dy)
                self.put_pixel(x0 + dx, y0 + dy, color)

    def _draw_textured_vertical_wall(
        self, x0, y0, length, texture, cell_x, cell_y, cell_size, thickness
    ):
        """Dessine un mur vertical avec texture continue."""
        if texture is None:
            self.draw_line_v(x0, y0, length, self.fallback_color, thickness)
            return

        for dx in range(thickness):
            for dy in range(length):
                global_y = (cell_y * cell_size) + dy
                color = self._get_pixel_from_texture(texture, dx, global_y)
                self.put_pixel(x0 + dx, y0 + dy, color)

    def render_with_textures(
        self,
        all_cell: list[Cell],
        WIDTH: int,
        HEIGHT: int,
        CELL_SIZE: int,
        OUTLINE_THICKNESS: int,
    ) -> None:
        """Rendu du labyrinthe avec textures."""

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cell = get_cell(all_cell, x, y, WIDTH)
                x0 = x * CELL_SIZE
                y0 = y * CELL_SIZE

                # ---- Mur horizontal HAUT ----
                if y == 0:
                    if cell.wall[0]:
                        self._draw_textured_horizontal_wall(
                            x0,
                            y0,
                            CELL_SIZE + OUTLINE_THICKNESS,
                            self.wall_textures["horizontal"],
                            x,
                            y,
                            CELL_SIZE,
                            OUTLINE_THICKNESS,
                        )
                else:
                    cell_above = get_cell(all_cell, x, y - 1, WIDTH)
                    if cell.wall[0] and not cell_above.wall[2]:
                        self._draw_textured_horizontal_wall(
                            x0,
                            y0,
                            CELL_SIZE + OUTLINE_THICKNESS,
                            self.wall_textures["horizontal"],
                            x,
                            y,
                            CELL_SIZE,
                            OUTLINE_THICKNESS,
                        )

                # ---- Mur horizontal BAS ----
                if cell.wall[2]:
                    self._draw_textured_horizontal_wall(
                        x0,
                        y0 + CELL_SIZE,
                        CELL_SIZE + OUTLINE_THICKNESS,
                        self.wall_textures["horizontal"],
                        x,
                        y,
                        CELL_SIZE,
                        OUTLINE_THICKNESS,
                    )

                # ---- Mur vertical GAUCHE ----
                if x == 0:
                    if cell.wall[3]:
                        self._draw_textured_vertical_wall(
                            x0,
                            y0,
                            CELL_SIZE + OUTLINE_THICKNESS,
                            self.wall_textures["vertical"],
                            x,
                            y,
                            CELL_SIZE,
                            OUTLINE_THICKNESS,
                        )
                else:
                    cell_left = get_cell(all_cell, x - 1, y, WIDTH)
                    if cell.wall[3] and not cell_left.wall[1]:
                        self._draw_textured_vertical_wall(
                            x0,
                            y0,
                            CELL_SIZE + OUTLINE_THICKNESS,
                            self.wall_textures["vertical"],
                            x,
                            y,
                            CELL_SIZE,
                            OUTLINE_THICKNESS,
                        )

                # ---- Mur vertical DROITE ----
                if cell.wall[1]:
                    self._draw_textured_vertical_wall(
                        x0 + CELL_SIZE,
                        y0,
                        CELL_SIZE + OUTLINE_THICKNESS,
                        self.wall_textures["vertical"],
                        x,
                        y,
                        CELL_SIZE,
                        OUTLINE_THICKNESS,
                    )

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self.img, 15, 15
        )

    def color_entry_and_exit(
        self, ENTRY_X: int, ENTRY_Y: int, EXIT_X: int, EXIT_Y: int
    ):
        """Colorie visuellement la cellule d'entrée et la cellule de sortie."""
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS

        for x in range(ENTRY_X, ENTRY_X + CELL_SIZE - OUTLINE_THICKNESS):
            for y in range(ENTRY_Y, ENTRY_Y + CELL_SIZE - OUTLINE_THICKNESS):
                self.put_pixel(x, y, 0xFF00FF00)
        for x in range(EXIT_X, EXIT_X + CELL_SIZE - OUTLINE_THICKNESS):
            for y in range(EXIT_Y, EXIT_Y + CELL_SIZE - OUTLINE_THICKNESS):
                self.put_pixel(x, y, 0xFFFF0000)

    def color_content_solver(
        self,
        all_cell: list[Cell],
        WIDTH: int,
        his_x: int,
        his_y: int,
        index: int,
        solver: list[tuple[int, int]],
        color: int,
    ):
        """Dessine un point et une connexion vers le suivant pour le solveur."""
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS

        cm = 5 // 2

        tmp_x = his_x * CELL_SIZE + OUTLINE_THICKNESS
        tmp_y = his_y * CELL_SIZE + OUTLINE_THICKNESS

        center_x = tmp_x + (CELL_SIZE - OUTLINE_THICKNESS) // 2
        center_y = tmp_y + (CELL_SIZE - OUTLINE_THICKNESS) // 2

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                self.put_pixel(center_x + dx, center_y + dy, color)

        if index < len(solver) - 1:
            next_x, next_y = solver[index + 1]

            next_center_x = (
                next_x * CELL_SIZE
                + OUTLINE_THICKNESS
                + (CELL_SIZE - OUTLINE_THICKNESS) // 2
            )
            next_center_y = (
                next_y * CELL_SIZE
                + OUTLINE_THICKNESS
                + (CELL_SIZE - OUTLINE_THICKNESS) // 2
            )

            if center_x == next_center_x:
                y1 = min(center_y, next_center_y)
                y2 = max(center_y, next_center_y)

                for x in range(center_x - cm, cm + center_x):
                    for y in range(y1, y2 + 1):
                        self.put_pixel(x, y, color)

            else:
                x1 = min(center_x, next_center_x)
                x2 = max(center_x, next_center_x)

                for x in range(x1, x2 + 1):
                    for y in range(center_y - cm, cm + center_y):
                        self.put_pixel(x, y, color)

    def color_isoler(
        self,
        isoler: list[tuple[int, int]],
        cell_iso: tuple[int, int],
        color: int,
    ):
        """Colorie une cellule isolée et ses éventuelles jonctions."""
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS

        iso_x, iso_y = cell_iso
        px = iso_x * CELL_SIZE + OUTLINE_THICKNESS
        py = iso_y * CELL_SIZE + OUTLINE_THICKNESS
        for x in range(px, px + CELL_SIZE - OUTLINE_THICKNESS):
            for y in range(py, py + CELL_SIZE - OUTLINE_THICKNESS):
                self.put_pixel(x, y, color)

        if (iso_x + 1, iso_y) in isoler:
            for dy in range(CELL_SIZE - OUTLINE_THICKNESS):
                for t in range(OUTLINE_THICKNESS + 1):
                    self.put_pixel(
                        px + CELL_SIZE - OUTLINE_THICKNESS + t,
                        py + dy,
                        color,
                    )

        if (iso_x - 1, iso_y) in isoler:
            for dy in range(CELL_SIZE - OUTLINE_THICKNESS):
                for t in range(OUTLINE_THICKNESS + 1):
                    self.put_pixel(px - t, py + dy, color)

        if (iso_x, iso_y + 1) in isoler:
            for dx in range(CELL_SIZE - OUTLINE_THICKNESS):
                for t in range(OUTLINE_THICKNESS + 1):
                    self.put_pixel(
                        px + dx,
                        py + CELL_SIZE - OUTLINE_THICKNESS + t,
                        color,
                    )

        if (iso_x, iso_y - 1) in isoler:
            for dx in range(CELL_SIZE - OUTLINE_THICKNESS):
                for t in range(OUTLINE_THICKNESS + 1):
                    self.put_pixel(px + dx, py - t, color)

    def clear_img(self):
        """Remplit l'image avec la couleur noire."""
        black = 0xFF000000
        for y in range(self.ROWS):
            for x in range(self.COLS):
                self.put_pixel(x, y, black)

    def render(
        self,
        all_cell: list[Cell],
        color: int,
    ) -> None:
        """Rendu complet des murs du labyrinthe dans l'image (version couleur)."""
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS

        for c in all_cell:
            x0 = c.x * CELL_SIZE
            y0 = c.y * CELL_SIZE

            if c.wall[0]:
                self.draw_line_h(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    color,
                    OUTLINE_THICKNESS,
                )
            if c.wall[1]:
                self.draw_line_v(
                    x0 + CELL_SIZE,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    color,
                    OUTLINE_THICKNESS,
                )
            if c.wall[2]:
                self.draw_line_h(
                    x0,
                    y0 + CELL_SIZE,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    color,
                    OUTLINE_THICKNESS,
                )
            if c.wall[3]:
                self.draw_line_v(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    color,
                    OUTLINE_THICKNESS,
                )

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self.img, 15, 15
        )

    def draw_cell(
        self,
        cell: Cell,
        color: int,
    ) -> None:
        """Dessine les murs d'une seule cellule (version couleur)."""
        from a_maze_ing import CELL_SIZE, OUTLINE_THICKNESS

        x0 = cell.x * CELL_SIZE
        y0 = cell.y * CELL_SIZE

        if cell.wall[0]:
            self.draw_line_h(
                x0,
                y0,
                CELL_SIZE + OUTLINE_THICKNESS,
                color,
                OUTLINE_THICKNESS,
            )
        if cell.wall[1]:
            self.draw_line_v(
                x0 + CELL_SIZE,
                y0,
                CELL_SIZE + OUTLINE_THICKNESS,
                color,
                OUTLINE_THICKNESS,
            )
        if cell.wall[2]:
            self.draw_line_h(
                x0,
                y0 + CELL_SIZE,
                CELL_SIZE + OUTLINE_THICKNESS,
                color,
                OUTLINE_THICKNESS,
            )
        if cell.wall[3]:
            self.draw_line_v(
                x0,
                y0,
                CELL_SIZE + OUTLINE_THICKNESS,
                color,
                OUTLINE_THICKNESS,
            )

    def draw_cell_with_texture(
        self,
        cell: Cell,
        WIDTH: int,
        HEIGHT: int,
        CELL_SIZE: int,
        OUTLINE_THICKNESS: int,
        all_cell: list[Cell],
    ) -> None:
        """Dessine une seule cellule avec textures."""

        x0 = cell.x * CELL_SIZE
        y0 = cell.y * CELL_SIZE

        # ---- Mur horizontal HAUT ----
        if cell.y == 0:
            if cell.wall[0]:
                self._draw_textured_horizontal_wall(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    self.wall_textures["horizontal"],
                    cell.x,
                    cell.y,
                    CELL_SIZE,
                    OUTLINE_THICKNESS,
                )
        else:
            cell_above = get_cell(all_cell, cell.x, cell.y - 1, WIDTH)
            if cell.wall[0] and not cell_above.wall[2]:
                self._draw_textured_horizontal_wall(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    self.wall_textures["horizontal"],
                    cell.x,
                    cell.y,
                    CELL_SIZE,
                    OUTLINE_THICKNESS,
                )

        # ---- Mur horizontal BAS ----
        if cell.wall[2]:
            self._draw_textured_horizontal_wall(
                x0,
                y0 + CELL_SIZE,
                CELL_SIZE + OUTLINE_THICKNESS,
                self.wall_textures["horizontal"],
                cell.x,
                cell.y,
                CELL_SIZE,
                OUTLINE_THICKNESS,
            )

        # ---- Mur vertical GAUCHE ----
        if cell.x == 0:
            if cell.wall[3]:
                self._draw_textured_vertical_wall(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    self.wall_textures["vertical"],
                    cell.x,
                    cell.y,
                    CELL_SIZE,
                    OUTLINE_THICKNESS,
                )
        else:
            cell_left = get_cell(all_cell, cell.x - 1, cell.y, WIDTH)
            if cell.wall[3] and not cell_left.wall[1]:
                self._draw_textured_vertical_wall(
                    x0,
                    y0,
                    CELL_SIZE + OUTLINE_THICKNESS,
                    self.wall_textures["vertical"],
                    cell.x,
                    cell.y,
                    CELL_SIZE,
                    OUTLINE_THICKNESS,
                )

        # ---- Mur vertical DROITE ----
        if cell.wall[1]:
            self._draw_textured_vertical_wall(
                x0 + CELL_SIZE,
                y0,
                CELL_SIZE + OUTLINE_THICKNESS,
                self.wall_textures["vertical"],
                cell.x,
                cell.y,
                CELL_SIZE,
                OUTLINE_THICKNESS,
            )
