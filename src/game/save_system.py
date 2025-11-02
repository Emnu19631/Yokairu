import json
import os
from datetime import datetime

SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "saves", "savegame.json")

def _leer_todos():
    """Devuelve lista de saves (posiblemente vacía). Maneja JSON corrupto."""
    if not os.path.exists(SAVE_PATH):
        return []
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, ValueError):
        # archivo corrupto -> tratar como sin saves
        return []

def _escribir_todos(lista):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def guardar_partida(slide_index):
    """Agrega un nuevo slot con timestamp y id incremental."""
    lista = _leer_todos()
    next_id = max([item.get("id", 0) for item in lista], default=0) + 1
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo = {
        "id": next_id,
        "slide": int(slide_index),
        "fecha": ahora
    }
    lista.append(nuevo)
    _escribir_todos(lista)
    return nuevo

def listar_guardados():
    """Devuelve la lista completa ordenada por fecha (más reciente al final)."""
    lista = _leer_todos()
    # Intento intentar ordenar por fecha si existe (sino por id)
    try:
        lista_sorted = sorted(lista, key=lambda x: x.get("fecha", ""), reverse=True)
    except Exception:
        lista_sorted = lista
    return lista_sorted

def cargar_partida_por_id(slot_id):
    """Devuelve el slot con id especificado o None."""
    lista = _leer_todos()
    for item in lista:
        if item.get("id") == slot_id:
            return item
    return None

def hay_partida_guardada():
    lista = _leer_todos()
    return len(lista) > 0
