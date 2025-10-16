import sys
import os
import pytest

# Agregar carpeta scripts al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from config import actualizar_resolucion, ANCHO_BASE, ALTO_BASE

def test_actualizar_resolucion():
    # Guardar valores originales
    from config import ANCHO, ALTO
    ancho_original = ANCHO
    alto_original = ALTO
    
    # Cambiar resolución
    actualizar_resolucion(1280, 720)
    from config import ANCHO, ALTO
    assert ANCHO == 1280
    assert ALTO == 720
    
    # Restaurar original
    actualizar_resolucion(ancho_original, alto_original)
