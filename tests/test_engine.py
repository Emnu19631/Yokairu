import pytest
import pygame
from unittest.mock import MagicMock, patch
from game import engine


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_crear_botones_navegacion_devuelve_dos_botones():
    fuente = pygame.font.SysFont("Arial", 20)
    boton_inicio, boton_ajustes = engine.crear_botones_navegacion(800, fuente)
    assert boton_inicio is not None
    assert boton_ajustes is not None
    assert boton_inicio.texto == "Inicio"
    assert boton_ajustes.texto == "Ajustes"


def test_dibujar_botones_navegacion_llama_dibujar(monkeypatch):
    mock_boton_inicio = MagicMock()
    mock_boton_ajustes = MagicMock()
    ventana = MagicMock()
    mouse_pos = (100, 100)
    engine.dibujar_botones_navegacion(ventana, mouse_pos, mock_boton_inicio, mock_boton_ajustes)
    mock_boton_inicio.dibujar.assert_called_once_with(ventana, mouse_pos)
    mock_boton_ajustes.dibujar.assert_called_once_with(ventana, mouse_pos)


@patch("game.engine.Boton")
def test_manejar_opciones_horizontal(mock_boton):
    slide = {
        "tipo": "eleccion",
        "opciones": [{"texto": "Opcion 1", "next": 1}, {"texto": "Opcion 2", "next": 2}],
        "layout": "horizontal"
    }
    botones, rect, color = engine.manejar_opciones(slide, 800, 600)
    assert isinstance(botones, list)
    assert len(botones) == 2
    assert isinstance(rect, pygame.Rect)
    assert isinstance(color, tuple)


@patch("game.engine.Boton")
def test_manejar_opciones_vertical(mock_boton):
    slide = {
        "tipo": "eleccion",
        "opciones": [
            {"texto": "Arriba Izq", "next": 1},
            {"texto": "Arriba Der", "next": 2},
            {"texto": "Abajo Izq", "next": 3},
            {"texto": "Abajo Der", "next": 4},
        ],
        "layout": "vertical"
    }
    botones, rect, color = engine.manejar_opciones(slide, 800, 600)
    assert len(botones) == 4
    assert isinstance(rect, pygame.Rect)
    assert isinstance(color, tuple)


@patch("game.engine.pygame.event.get", return_value=[MagicMock(type=pygame.QUIT)])
def test_manejar_eventos_devuelve_salir(mock_eventos):
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()
    botones_opciones = []
    res = engine._manejar_eventos(boton_inicio, boton_ajustes, botones_opciones, 0)
    assert res == "salir"


@patch("game.engine.pygame.event.get", return_value=[MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10))])
def test_manejar_eventos_click_inicio(mock_eventos):
    boton_inicio = MagicMock(es_click=MagicMock(return_value=True))
    boton_ajustes = MagicMock()
    botones_opciones = []
    res = engine._manejar_eventos(boton_inicio, boton_ajustes, botones_opciones, 0)
    assert res == "inicio"


def test_procesar_click_en_opciones():
    boton_inicio = MagicMock(es_click=MagicMock(return_value=False))
    boton_ajustes = MagicMock(es_click=MagicMock(return_value=False))
    boton_opcion = MagicMock(es_click=MagicMock(return_value=True))
    botones = [(boton_opcion, "next_slide")]
    res = engine._procesar_click((10, 10), boton_inicio, boton_ajustes, botones, 0)
    assert res == "next_slide"


def test_cargar_y_dibujar_imagen_con_imagen(monkeypatch):
    # ✅ Superficie real, no MagicMock
    surface = pygame.Surface((100, 100))
    monkeypatch.setattr(engine, "cargar_imagen", MagicMock(return_value=surface))

    ventana = pygame.Surface((800, 600))
    result = engine.cargar_y_dibujar_imagen({"imagen": "foto.png"}, ventana, 800, 600)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pygame.Surface) or result[0] is None


def test_cargar_y_dibujar_imagen_sin_imagen():
    ventana = pygame.Surface((800, 600))
    res = engine.cargar_y_dibujar_imagen({}, ventana, 800, 600)
    assert res == (None, None)
