import pygame
import sys
import json
import os

SAVE_PATH = "saves/savegame.json"

# Guarda la partida en un archivo JSON
def guardar_partida(data):
    os.makedirs("saves", exist_ok=True)  # Crea la carpeta si no existe
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f, indent=4)  # Escribe los datos de la partida
    print("✅ Partida guardada correctamente.")

# Carga la partida desde el archivo JSON
def cargar_partida():
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)  # Carga los datos guardados
        print("✅ Partida cargada:", data)
        return data
    else:
        print("⚠️ No existe una partida guardada.")
        return None
