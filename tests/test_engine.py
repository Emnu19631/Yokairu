import pytest
import pygame
from unittest.mock import MagicMock, patch
from game import engine


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


# ===============================
# TESTS EXISTENTES
# ===============================

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


# ===============================
# NUEVOS TESTS
# ===============================

@patch("game.engine.HISTORIA", [{"tipo": "narracion", "next": 1}, {"tipo": "eleccion", "opciones": [{"texto": "Opción 1", "next": 2}]}])
@patch("game.engine.crear_botones_navegacion")
@patch("game.engine.preparar_fondo")
@patch("game.engine.procesar_narracion")
@patch("game.engine.procesar_eleccion")
@patch("game.engine.guardar_partida")
def test_ejecutar_novela(mock_guardar, mock_proc_eleccion, mock_proc_narracion, mock_preparar, mock_crear):
    mock_crear.return_value = (MagicMock(), MagicMock())
    mock_guardar.return_value = {"id": 1}
    mock_proc_narracion.return_value = (None, 1)
    mock_proc_eleccion.return_value = (None, 2)
    ventana = MagicMock()
    fuente = MagicMock()
    res = engine.ejecutar_novela(ventana, fuente, 800, 600)
    assert res == "menu"


@patch("game.engine.cargar_imagen")
def test_preparar_fondo(mock_cargar):
    mock_cargar.return_value = MagicMock(spec=pygame.Surface)
    ventana = MagicMock()
    slide = {"fondo": "fondo.png"}
    fondo = engine.preparar_fondo(slide, ventana, 800, 600)
    assert fondo is not None
    mock_cargar.assert_called_once_with("fondo.png", 800, 600)


@patch("pygame.display.update")  # 🧩 Evita error de "Display mode not set"
@patch("pygame.mouse.get_pos", return_value=(0, 0))
@patch("game.engine.manejar_texto_y_botones")
@patch("game.engine.dibujar_botones_navegacion")
@patch("game.engine.cargar_y_dibujar_imagen")
def test_procesar_narracion(mock_cargar_img, mock_dibujar, mock_manejar, mock_mouse, mock_display):
    mock_cargar_img.return_value = (None, None)
    mock_manejar.return_value = None
    slide = {"tipo": "narracion", "next": 1}
    ventana = MagicMock()
    fuente = MagicMock()
    fondo = MagicMock()
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()
    _, idx = engine.procesar_narracion(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, 800, 600, 0)
    assert idx == 1

    mock_display.assert_called_once()  # ✅ confirma que se llamó al update


@patch("pygame.display.update")
@patch("pygame.mouse.get_pos", return_value=(0, 0))
@patch("pygame.event.get", return_value=[MagicMock(type=pygame.QUIT)])  # evita bucle
@patch("game.engine.manejar_opciones")
@patch("game.engine.dibujar_botones_navegacion")
@patch("game.engine.cargar_y_dibujar_imagen")
def test_procesar_eleccion(mock_cargar_img, mock_dibujar, mock_manejar_op, mock_event, mock_mouse, mock_display):
    mock_cargar_img.return_value = (None, None)
    mock_manejar_op.return_value = ([], pygame.Rect(0, 0, 100, 100), (255, 255, 255))

    ventana = pygame.Surface((800, 600))
    slide = {"tipo": "eleccion", "opciones": [{"texto": "Opción 1", "next": 2}]}
    fuente = MagicMock()
    fondo = pygame.Surface((800, 600))
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()

    _, idx = engine.procesar_eleccion(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, 800, 600, 0)

    assert isinstance(idx, int)
    mock_display.assert_called()  # 👈 se permite más de una llamada






@patch("pygame.event.get")
def test_manejar_eventos_texto(mock_event_get):
    mock_event_get.return_value = [MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10))]
    boton_inicio = MagicMock(es_click=MagicMock(return_value=True))
    boton_ajustes = MagicMock()
    accion = engine._manejar_eventos_texto(boton_inicio, boton_ajustes)
    assert accion == "inicio"


@patch("pygame.event.get")
def test_esperar_confirmacion_final(mock_event_get):
    mock_event_get.return_value = [MagicMock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10))]
    boton_inicio = MagicMock(es_click=MagicMock(return_value=True))
    boton_ajustes = MagicMock()
    res = engine._esperar_confirmacion_final(boton_inicio, boton_ajustes)
    assert res == "inicio"


# test_engine.py

def test_mostrar_texto_con_botones_visibles():
    class FuenteMock:
        def get_height(self):
            return 20
        def render(self, texto, aa, color):
            return pygame.Surface((50, 20))
    
    ventana = pygame.Surface((800, 600))
    fondo = pygame.Surface((800, 600))
    fuente = FuenteMock()
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()
    rect = pygame.Rect(0, 0, 100, 50)

    with patch("pygame.display.update") as mock_display, \
         patch("pygame.mouse.get_pos", return_value=(0, 0)), \
         patch("game.engine._esperar_confirmacion_final", return_value="inicio"), \
         patch("game.engine._actualizar_texto", side_effect=lambda t, m, i, c, tt: (t, len(t), True, tt)), \
         patch("game.engine._manejar_eventos_texto", return_value=None):

        res = engine.mostrar_texto_con_botones_visibles(
            ventana, fuente, "Hola", (0, 0, 0), rect, fondo, boton_inicio, boton_ajustes
        )

    assert res == "inicio"
    mock_display.assert_called()

# ------------------------------
def test_actualizar_texto_avanza_y_completa(monkeypatch):
    start = 1000
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: start + 100)

    texto = "AB"
    mostrado, indice, completo, _ = engine._actualizar_texto(texto, "", 0, False, start)
    assert mostrado == "A"
    assert indice == 1
    assert not completo




@patch("core.render.ajustar_fuente_al_rect", return_value=(MagicMock(get_height=lambda: 10, render=lambda t, a, c: pygame.Surface((10, 10))), ["Hola"]))
@patch("pygame.display.update")
@patch("pygame.mouse.get_pos", return_value=(0, 0))
def test_dibujar_pantalla_texto(mock_mouse, mock_display, mock_ajustar):
    ventana = pygame.Surface((200, 200))
    fondo = pygame.Surface((200, 200))
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()
    fuente = MagicMock()
    rect = pygame.Rect(0, 0, 100, 50)
    engine._dibujar_pantalla_texto(ventana, fondo, None, None, boton_inicio, boton_ajustes, fuente, "Hola", (0, 0, 0), rect)
    mock_display.assert_called()
    boton_inicio.dibujar.assert_called_once()
    boton_ajustes.dibujar.assert_called_once()


def test_procesar_click_fuera_de_botones():
    boton_inicio = MagicMock(es_click=MagicMock(return_value=False))
    boton_ajustes = MagicMock(es_click=MagicMock(return_value=False))
    boton_opcion = MagicMock(es_click=MagicMock(return_value=False))
    botones = [(boton_opcion, "next_slide")]
    res = engine._procesar_click((999, 999), boton_inicio, boton_ajustes, botones, 0)
    assert res is None


@patch("game.engine.Boton")
def test_manejar_opciones_layout_desconocido(mock_boton):
    slide = {
        "tipo": "eleccion",
        "opciones": [{"texto": "Opción 1", "next": 1}],
        "layout": "diagonal"  # layout que no existe
    }
    botones, rect, color = engine.manejar_opciones(slide, 800, 600)
    assert isinstance(botones, list)
    assert isinstance(rect, pygame.Rect)
    assert isinstance(color, tuple)



def test_actualizar_texto_completo():
    texto = "AB"
    mostrado, indice, completo, start_time = engine._actualizar_texto(texto, "AB", 2, True, 0)
    assert mostrado == "AB"
    assert indice == 2
    assert completo


from unittest.mock import MagicMock, patch
import pygame
from game import engine

def test_manejar_texto_y_botones_todas_rutas():
    ventana = MagicMock()
    fuente = MagicMock()
    fondo = MagicMock()
    boton_inicio = MagicMock()
    boton_ajustes = MagicMock()
    img = MagicMock()
    pos = (0, 0)
    slide_index = 3
    ancho, alto = 800, 600

    # 1️⃣ Slide sin texto → retorna None
    slide = {}
    assert engine.manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index) is None

    slide = {"texto": "Hola mundo"}

    # Mockeamos mostrar_texto_con_botones_visibles
    with patch("game.engine.mostrar_texto_con_botones_visibles", return_value="inicio"):
        assert engine.manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index) == "inicio"

    with patch("game.engine.mostrar_texto_con_botones_visibles", return_value="ajustes"):
        assert engine.manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index) == f"ajustes:{slide_index}"

    with patch("game.engine.mostrar_texto_con_botones_visibles", return_value=True):
        assert engine.manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index) == "salir"

    with patch("game.engine.mostrar_texto_con_botones_visibles", return_value=None):
        assert engine.manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index) is None

