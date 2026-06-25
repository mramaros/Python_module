#!/usr/bin/env python3
# ########################################################################### #
#   mazegen/key_maps.py                                                       #
# ########################################################################### #

import sys

ENVIRONMENTS = ["normal", "sable", "donjon", "lave", "glace"]


def handle_keypress(keycode, state):
    """
    Gère les entrées clavier de base :
    - '3' (51 ou 20) : Change d'environnement et relance l'animation.
    - ESC ou '4'     : Quitte le programme.
    """
    # Touche '3'
    if keycode in (51, 20):
        current_idx = state.get("env_idx", 0)
        next_idx = (current_idx + 1) % len(ENVIRONMENTS)
        state["env_idx"] = next_idx
        new_env = ENVIRONMENTS[next_idx]

        print(f"\n🌍 Changement d'environnement -> '{new_env.upper()}'")

        state["my_window"].change_environment(new_env)

        state["anime"].clear()
        state["anime"].extend(state["backup_anime"])
        state["isoler"].clear()
        state["isoler"].extend(state["backup_isoler"])
        state["solver"].clear()
        state["solver"].extend(state["backup_solver"])

        state["already_printed"][0] = False
        state["my_window"].clear_img()
        state["my_window"].fill_all_ground(state["WIDTH"], state["HEIGHT"])

        try:
            from .the_animations import anime_solv
            anime_solv.last_pos = None
        except ImportError:
            pass

    # Touche ESC (Linux: 65307, Mac: 53) ou '4' (21 ou 52)
    elif keycode in (65307, 53, 52, 21):
        print("\n👋 Fermeture d'A-Maze-ing. À bientôt !")
        sys.exit(0)


def custom_handle_keypress(keycode, state):
    """
    Couche étendue au-dessus de handle_keypress :
    - '3' : invalide le cache bg avant de déléguer à handle_keypress.
    - '2' : dessine / efface le solveur (machine à états).
    - Tout autre touche : délégué à handle_keypress.
    """
    # --- Touche '3' : changement de biome ---
    if keycode in (51, 20):
        if "clean_bg_data" in state:
            del state["clean_bg_data"]
        handle_keypress(keycode, state)
        state["solver"].clear()
        state["solver_state"] = "hidden"
        return

    # --- Touche '2' : toggle solveur ---
    if keycode in (50, 19):
        solver_state = state["solver_state"]

        if solver_state == "hidden":
            state["solver"] = list(state["backup_solver"])
            state["solver_state"] = "drawing"
            try:
                from mazegen.the_animations import anime_solv
                anime_solv.last_pos = None
            except ImportError:
                pass
            print("▶️ Dessin du solveur lancé...")

        elif solver_state == "drawing":
            state["erase_index"] = (
                len(state["backup_solver"]) - len(state["solver"])
            )
            state["solver"].clear()
            state["solver_state"] = "erasing"
            print("↩️ Interruption ! Effacement du solveur...")

        elif solver_state == "shown":
            state["erase_index"] = len(state["backup_solver"])
            state["solver_state"] = "erasing"
            print("↩️ Effacement du solveur lancé...")

        elif solver_state == "erasing":
            state["solver"] = state["backup_solver"][state["erase_index"]:]
            state["solver_state"] = "drawing"
            try:
                from mazegen.the_animations import anime_solv
                anime_solv.last_pos = state["backup_solver"][
                    max(0, state["erase_index"] - 1)
                ]
            except ImportError:
                pass
            print("▶️ Reprise du tracé du solveur...")
        return

    # --- Toutes les autres touches ---
    handle_keypress(keycode, state)
