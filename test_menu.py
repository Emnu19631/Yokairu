import sys
import os
import pygame
import pytest

# Agregar carpeta scripts al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from boton import Boton

pygame.init()

def test_boton_click():
    fuente = pygame.font.SysFont("Arial", 20)
    boton = Boton(50, 50, 100, 40, "Prueba", (255,255,255), (0,0,0), fuente)
    
    # Dentro del rectángulo
    assert boton.es_click((60, 60)) == True
    # Fuera del rectángulo
    assert boton.es_click((10, 10)) == False
