import pytest
import pygame
from unittest.mock import MagicMock

from game import engine


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_ajustar_tamano_boton_y_fuente_texto_corto():
    ancho, alto, fuente = engine.ajustar_tamano_boton_y_fuente("Hola")
    assert ancho == 200
    assert alto == 50
    assert fuente == 24


def test_ajustar_tamano_boton_y_fuente_texto_largo():
    ancho, alto, fuente = engine.ajustar_tamano_boton_y_fuente("Texto extremadamente largo de prueba")
    assert ancho > 200
    assert alto > 50
    assert fuente < 24


def test_crear_botones_navegacion():
    fuente = pygame.font.SysFont("Arial", 24)
    b_inicio, b_ajustes = engine.crear_botones_navegacion(800, fuente)
    assert b_inicio.texto == "Inicio"
    assert b_ajustes.texto == "Ajustes"


def test_procesar_click_devuelve_inicio(monkeypatch):
    boton_inicio = MagicMock()
    boton_inicio.es_click.return_value = True
    boton_ajustes = MagicMock()
    boton_ajustes.es_click.return_value = False

    resultado = engine._procesar_click((10, 10), boton_inicio, boton_ajustes, [], 0)
    assert resultado == "inicio"


def test_procesar_click_devuelve_ajustes(monkeypatch):
    boton_inicio = MagicMock()
    boton_inicio.es_click.return_value = False
    boton_ajustes = MagicMock()
    boton_ajustes.es_click.return_value = True

    resultado = engine._procesar_click((10, 10), boton_inicio, boton_ajustes, [], 1)
    assert resultado == "ajustes:1"


def test_procesar_click_devuelve_destino_opcion():
    boton_inicio = MagicMock()
    boton_inicio.es_click.return_value = False
    boton_ajustes = MagicMock()
    boton_ajustes.es_click.return_value = False

    boton_opcion = MagicMock()
    boton_opcion.es_click.return_value = True
    botones = [(boton_opcion, "siguiente")]

    resultado = engine._procesar_click((0, 0), boton_inicio, boton_ajustes, botones, 0)
    assert resultado == "siguiente"


def test_procesar_click_sin_clicks():
    boton_inicio = MagicMock()
    boton_inicio.es_click.return_value = False
    boton_ajustes = MagicMock()
    boton_ajustes.es_click.return_value = False
    botones = []

    resultado = engine._procesar_click((0, 0), boton_inicio, boton_ajustes, botones, 0)
    assert resultado is None
