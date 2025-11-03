import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.ui import cargar as cg


@pytest.fixture(scope="module", autouse=True)
def setup_pygame():
    """Inicializa pygame antes de los tests."""
    pygame.display.init()
    pygame.font.init()
    yield
    pygame.quit()


# ========================
# TEST _obtener_miniatura_para_slot
# ========================

@patch("src.ui.cargar.HISTORIA", [{"imagen": "test.png"}])
@patch("src.ui.cargar.cargar_imagen", return_value=pygame.Surface((100, 100)))
def test_obtener_miniatura_valida(mock_cargar):
    slot = {"slide": 0}
    mini = cg._obtener_miniatura_para_slot(slot)
    assert isinstance(mini, pygame.Surface)


@patch("src.ui.cargar.HISTORIA", [{}])
@patch("src.ui.cargar.cargar_imagen", side_effect=Exception("error"))
def test_obtener_miniatura_invalida(mock_cargar):
    slot = {"slide": 0}
    mini = cg._obtener_miniatura_para_slot(slot)
    assert mini is None


# ========================
# EVENTOS BÁSICOS
# ========================

def test_evento_quit_y_scroll():
    e_quit = MagicMock(type=pygame.QUIT)
    e_scroll = MagicMock(type=pygame.MOUSEWHEEL, y=-1)
    assert cg._evento_quit(e_quit) == "quit"
    assert cg._evento_quit(MagicMock(type=pygame.KEYDOWN)) is None
    assert cg._evento_scroll(e_scroll, 100) == "ok"


def test_slot_clicado_retorna_slide():
    boton = MagicMock()
    boton.es_click.return_value = True
    e = MagicMock(pos=(10, 10))
    with patch("src.ui.cargar.cargar_partida_por_id", return_value={"slide": 2}):
        result = cg._slot_clicado(e, boton, {"id": 1})
    assert result == 2


def test_slot_clicado_no_click():
    boton = MagicMock()
    boton.es_click.return_value = False
    e = MagicMock(pos=(0, 0))
    result = cg._slot_clicado(e, boton, {"id": 1})
    assert result == "ok"


def test_click_en_slots_dispara_evento():
    e = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10))
    boton = MagicMock()
    boton.rect = MagicMock(y=100, height=50)
    boton.es_click.return_value = True
    with patch("src.ui.cargar._slot_clicado", return_value=5):
        result = cg._click_en_slots(e, [(boton, {"id": 1})], 0, 200)
    assert result == 5


def test_click_volver_detecta_click():
    e = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10))
    boton = MagicMock()
    boton.es_click.return_value = True
    result = cg._click_volver(e, boton)
    assert result is None


# ========================
# RESIZE y EVENTOS COMPLETOS
# ========================

@patch("src.ui.cargar.cargar_imagen", return_value=pygame.Surface((100, 100)))
@patch("src.ui.cargar.actualizar_resolucion")
def test_evento_resize(mock_res, mock_img):
    e = MagicMock(type=pygame.VIDEORESIZE, size=(800, 600))
    cg._evento_resize(e)
    mock_res.assert_called_once()
    mock_img.assert_called_once()


@patch("src.ui.cargar._evento_quit", return_value=None)
@patch("src.ui.cargar._evento_scroll")
@patch("src.ui.cargar._click_en_slots", return_value="ok")
@patch("src.ui.cargar._click_volver", return_value="ok")
@patch("src.ui.cargar._evento_resize")
@patch("src.ui.cargar.pygame.event.get", return_value=[MagicMock()])
def test_procesar_eventos(mock_get, *_):
    boton_volver = MagicMock()
    result = cg._procesar_eventos(100, [], 0, 200, boton_volver)
    assert result == "continuar"


# ========================
# DIBUJAR (solo el título)
# ========================

def test_dibujar_titulo_sin_error():
    cg.ventana = pygame.display.set_mode((300, 200))
    cg.ANCHO, cg.ALTO = 300, 200
    fuente = pygame.font.SysFont("Arial", 20)
    cg._dibujar_titulo(fuente)  # No debe lanzar error


# ========================
# PANTALLA PRINCIPAL
# ========================

@patch("src.ui.cargar.listar_guardados", return_value=[])
@patch("src.ui.cargar.cargar_imagen", return_value=pygame.Surface((100, 100)))
@patch("src.ui.cargar._procesar_eventos", return_value="quit")
def test_pantalla_cargar_sale_correctamente(mock_proc, *_):
    cg.ventana = pygame.display.set_mode((200, 200))
    fuente = pygame.font.SysFont("Arial", 20)
    result = cg.pantalla_cargar(fuente)
    assert result is None


# ========================
# TEST _dibujar_slots
# ========================

@patch("src.ui.cargar._obtener_miniatura_para_slot", return_value=pygame.Surface((140, 80)))
def test_dibujar_slots_dibuja_bien(mock_miniatura):
    cg.ventana = pygame.display.set_mode((400, 300))
    cg.ANCHO, cg.ALTO = 400, 300
    fuente = pygame.font.SysFont("Arial", 20)
    mouse_pos = (0, 0)

    # Creamos un "save" de prueba con fecha y slide
    saves = [{"slide": 0, "fecha": "2025-11-02T15:30:00"}]

    botones_slots = cg._dibujar_slots(
        saves=saves,
        fuente=fuente,
        mouse_pos=mouse_pos,
        limite_superior=50,
        limite_inferior=250,
        slot_h=100,
        espacio_total=120,
        start_y=60,
        ancho_slot=300,
        x_slot=50
    )

    # Verificamos que se haya creado un botón y devuelto en la lista
    assert len(botones_slots) == 1
    boton, slot = botones_slots[0]
    assert slot["slide"] == 0
    # Verificamos que el botón tenga un rect dentro de la ventana
    assert 0 <= boton.rect.x <= cg.ANCHO
    assert 0 <= boton.rect.y <= cg.ALTO
