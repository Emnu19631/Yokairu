import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.ui import ajustes as aj
from src.ui.boton import Boton


@pytest.fixture(scope="module", autouse=True)
def setup_pygame():
    """Inicializa todos los módulos necesarios de pygame para los tests."""
    pygame.display.init()
    pygame.font.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        # En entornos de CI o sin salida de audio, usar un mock
        pygame.mixer.init = MagicMock()
        pygame.mixer.music = MagicMock()
    yield
    pygame.quit()


def crear_botones(fuente):
    b1 = Boton(0, 0, 100, 50, "+", (255, 255, 255), (0, 0, 0), fuente)
    b2 = Boton(0, 0, 100, 50, "-", (255, 255, 255), (0, 0, 0), fuente)
    b3 = Boton(0, 0, 100, 50, "Pantalla Completa: OFF", (255, 255, 255), (0, 0, 0), fuente)
    b4 = Boton(0, 0, 100, 50, "Volver", (255, 255, 255), (0, 0, 0), fuente)
    return [b1, b2, b3, b4]


def test_manejar_evento_click_volumen_mas():
    pygame.mixer.music.set_volume = MagicMock()
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)

    evento = MagicMock(pos=(10, 10))
    botones[0].es_click = MagicMock(return_value=True)
    for i in [1, 2, 3]:
        botones[i].es_click = MagicMock(return_value=False)

    res, _, _, _, nuevo_vol, _ = aj.manejar_evento_click(evento, botones, 0.5, False)
    assert 0.5 < nuevo_vol <= 1.0
    assert res in (None, "continuar", "volver")
    pygame.mixer.music.set_volume.assert_called_once()


def test_manejar_evento_click_volumen_menos():
    pygame.mixer.music.set_volume = MagicMock()
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)

    evento = MagicMock(pos=(10, 10))
    botones[1].es_click = MagicMock(return_value=True)
    for i in [0, 2, 3]:
        botones[i].es_click = MagicMock(return_value=False)

    res, _, _, _, nuevo_vol, _ = aj.manejar_evento_click(evento, botones, 0.5, False)
    assert 0.0 <= nuevo_vol < 0.5
    assert res in (None, "continuar", "volver")


@patch("src.ui.ajustes.actualizar_resolucion")
@patch("src.ui.ajustes.cargar_imagen", return_value=MagicMock())
def test_manejar_evento_click_pantalla(mock_img, mock_res):
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)
    for b in botones:
        b.es_click = MagicMock(return_value=False)
    botones[2].es_click.return_value = True

    evento = MagicMock(pos=(10, 10))
    res, *_ , nueva_pc = aj.manejar_evento_click(evento, botones, 0.5, False)
    assert isinstance(nueva_pc, bool)
    assert res in (None, "continuar", "volver")
    mock_res.assert_called_once()
    mock_img.assert_called_once()


def test_manejar_evento_click_volver():
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)
    for b in botones:
        b.es_click = MagicMock(return_value=False)
    botones[3].es_click.return_value = True

    evento = MagicMock(pos=(10, 10))
    resultado, *_ = aj.manejar_evento_click(evento, botones, 0.5, False)
    assert resultado == "volver"


def test_manejar_evento_click_sin_accion():
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)
    for b in botones:
        b.es_click = MagicMock(return_value=False)

    evento = MagicMock(pos=(999, 999))
    resultado, *_ = aj.manejar_evento_click(evento, botones, 0.5, False)
    assert resultado is None


def test_dibujar_pantalla_sin_error():
    ventana = pygame.display.set_mode((200, 200))
    fuente = pygame.font.SysFont("Arial", 20)
    botones = crear_botones(fuente)
    aj.ventana = ventana
    aj.fondo = pygame.Surface((200, 200))
    aj.ANCHO, aj.ALTO = 200, 200

    aj.dibujar_pantalla(0.5, 1.0, 1.0, botones)
    pygame.display.quit()


@patch("src.ui.ajustes.cargar_imagen", return_value=pygame.Surface((200, 200)))
@patch("src.ui.ajustes.dibujar_pantalla")
@patch("pygame.event.get")
def test_pantalla_ajustes_volver(mock_event_get, mock_dibujar, mock_cargar_imagen):
    fuente = pygame.font.SysFont("Arial", 20)

    # Simula un solo clic en el botón "Volver"
    mock_event_get.return_value = [
        MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0))
    ]

    # Mock de manejar_evento_click para devolver "volver"
    with patch("src.ui.ajustes.manejar_evento_click", return_value=("volver", None, None, None, 0.5, False)):
        resultado = aj.pantalla_ajustes(fuente)

    # Verifica que la función retorna correctamente
    assert isinstance(resultado, tuple)
    assert resultado[0] == "volver"
