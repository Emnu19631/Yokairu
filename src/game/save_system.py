import json
import os

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "saves", "savegame.json")

# ===============================
# FUNCIONES PRINCIPALES
# ===============================

def guardar_partida(data):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def cargar_partida():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            return json.load(f)
    return None
