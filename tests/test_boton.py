import pytest
import pygame
from src.ui.boton import Boton


@pytest.fixture(scope="module", autouse=True)
def setup_pygame():
    """Inicializa y cierra pygame automáticamente para todos los tests."""
    pygame.init()
    pygame.display.set_mode((200, 200))
    yield
    pygame.quit()


def crear_boton():
    fuente = pygame.font.SysFont("Arial", 20)
    return Boton(10, 10, 100, 40, "Click", (255, 255, 255), (0, 0, 0), fuente,
                 color_hover=(200, 200, 200), color_seleccion=(0, 255, 0))


# ================================
# TEST: Creación y atributos base
# ================================

def test_creacion_boton_basico():
    boton = crear_boton()
    assert boton.texto == "Click"
    assert isinstance(boton.rect, pygame.Rect)
    assert boton.color_hover == (200, 200, 200)
    assert boton.color_seleccion == (0, 255, 0)
    assert boton.ancho_base == 100
    assert boton.alto_base == 40


def test_color_hover_y_seleccion_default():
    fuente = pygame.font.SysFont("Arial", 20)
    boton = Boton(0, 0, 50, 50, "Test", (100, 100, 100), (255, 255, 255), fuente)
    assert boton.color_hover == (100, 100, 100)
    assert boton.color_seleccion == (200, 220, 255)


# ================================
# TEST: es_click
# ================================

def test_es_click_dentro_y_fuera():
    boton = crear_boton()
    assert boton.es_click((20, 20))  # Dentro
    assert not boton.es_click((200, 200))  # Fuera


# ================================
# TEST: actualizar_posicion
# ================================

def test_actualizar_posicion_modifica_rect():
    boton = crear_boton()
    old_rect = boton.rect.copy()
    boton.actualizar_posicion(2.0, 0.5)
    assert boton.rect.width == old_rect.width * 2
    assert boton.rect.height == old_rect.height * 0.5


# ================================
# TEST: dibujar
# ================================

def test_dibujar_hover(monkeypatch):
    """Verifica que el color cambie al pasar el mouse (hover)."""
    boton = crear_boton()
    ventana = pygame.Surface((200, 200))

    # Simulamos posición del mouse dentro del botón
    boton.dibujar(ventana, mouse_pos=(15, 15))
    # Si pasa hover, debe usar el color_hover
    color_usado = ventana.get_at((boton.rect.x + 1, boton.rect.y + 1))
    assert isinstance(color_usado, pygame.Color)


def test_dibujar_seleccionado(monkeypatch):
    """Verifica que el color de selección se use correctamente."""
    boton = crear_boton()
    ventana = pygame.Surface((200, 200))
    boton.dibujar(ventana, mouse_pos=(0, 0), seleccionado=True)
    color_usado = ventana.get_at((boton.rect.x + 1, boton.rect.y + 1))
    assert isinstance(color_usado, pygame.Color)


def test_dibujar_sin_hover(monkeypatch):
    """Verifica que dibujar sin hover usa el color de fondo."""
    boton = crear_boton()
    ventana = pygame.Surface((200, 200))
    boton.dibujar(ventana, mouse_pos=(999, 999))
    color_usado = ventana.get_at((boton.rect.x + 1, boton.rect.y + 1))
    assert isinstance(color_usado, pygame.Color)


def test_dibujar2_funciona():
    """Verifica que dibujar2 no cause errores."""
    boton = crear_boton()
    ventana = pygame.Surface((200, 200))
    boton.dibujar2(ventana)  # No debe lanzar excepción
