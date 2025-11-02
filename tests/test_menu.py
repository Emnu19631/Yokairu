import pytest
import pygame
from unittest.mock import patch, MagicMock
from ui import menu

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_crear_botones_devuelve_lista_correcta(monkeypatch):
    fuente = pygame.font.SysFont("Arial", 34)
    monkeypatch.setattr(menu, "fuente", fuente)
    botones = menu.crear_botones()
    assert isinstance(botones, list)
    assert len(botones) == len(menu.botones_textos)
    assert [b.texto for b in botones] == menu.botones_textos

def test_crear_botones_actualiza_posicion(monkeypatch):
    mock_boton = MagicMock()
    mock_boton.side_effect = lambda *a, **kw: MagicMock(actualizar_posicion=MagicMock())

    with patch("ui.menu.Boton", mock_boton):
        botones = menu.crear_botones()

    assert len(botones) == len(menu.botones_textos)
    for boton in botones:
        boton.actualizar_posicion.assert_called_once()


def test_crear_botones_usa_escalas_correctas(monkeypatch):
    monkeypatch.setattr(menu, "ANCHO", 1600)
    monkeypatch.setattr(menu, "ALTO", 900)
    monkeypatch.setattr(menu, "ANCHO_BASE", 800)
    monkeypatch.setattr(menu, "ALTO_BASE", 450)
    mock_boton = MagicMock()
    with patch("ui.menu.Boton", mock_boton):
        menu.crear_botones()
    args, _ = mock_boton.call_args
    assert isinstance(args[0], int)
    assert isinstance(args[1], int)
    assert any(t in args for t in ["Iniciar", "Cargar", "Ajustes", "Salir"])

def test_fuente_inicial_es_arial():
    assert isinstance(menu.fuente, pygame.font.Font)

def test_botones_textos_contiene_opciones_correctas():
    assert menu.botones_textos == ["Iniciar", "Cargar", "Ajustes", "Salir"]
