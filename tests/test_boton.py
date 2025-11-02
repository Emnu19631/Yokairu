import pygame
from ui import boton

def test_boton_click():
    pygame.init()
    fuente = pygame.font.SysFont("Arial", 20)
    b = boton.Boton(0, 0, 100, 50, "Test", (255,255,255), (0,0,0), fuente)
    assert not b.es_click((-10, -10))
    assert b.es_click((10, 10))
    pygame.quit()

def test_boton_actualizar_posicion_y_dibujar():
    pygame.init()
    ventana = pygame.display.set_mode((200, 200))
    fuente = pygame.font.SysFont("Arial", 20)
    b = boton.Boton(10, 10, 100, 50, "Test", (255,255,255), (0,0,0), fuente)
    b.actualizar_posicion(1.5, 2.0)
    assert isinstance(b.rect, pygame.Rect)

    # Probar dibujar sin errores
    b.dibujar(ventana, mouse_pos=(15, 15))
    b.dibujar(ventana, mouse_pos=(500, 500))
    b.dibujar(ventana, mouse_pos=(15, 15), seleccionado=True)
    b.dibujar2(ventana)  # también cubrir dibujar2()

    pygame.display.quit()
    pygame.quit()
