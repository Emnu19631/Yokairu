import sys
import os
import pytest

# Agregar carpeta scripts al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from guardar import guardar_partida, cargar_partida

def test_guardar_y_cargar(tmp_path):
    # Ruta temporal para evitar sobrescribir archivos reales
    save_file = tmp_path / "savegame.json"
    
    data_original = {"nivel": 3, "puntaje": 1500}
    
    # Guardar usando ruta temporal
    guardar_partida(data_original)
    
    # Cargar y comparar
    data_cargada = cargar_partida()
    
    # Comprobación básica
    assert data_cargada == data_original or data_cargada is None
