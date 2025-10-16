import pygame
import sys
import json
import os


SAVE_PATH = "saves/savegame.json"

def guardar_partida(data):
    os.makedirs("saves", exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Partida guardada correctamente.")

def cargar_partida():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
        print("✅ Partida cargada:", data)
        return data
    else:
        print("⚠️ No existe una partida guardada.")
        return None
