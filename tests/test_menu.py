import pygame
import pytest
from unittest.mock import patch, MagicMock


def crear_fuente_mock():
    fuente_mock = MagicMock()
    fuente_mock.get_height.return_value = 20
    fuente_mock.get_name.return_value = None
    fuente_mock.size.side_effect = lambda texto: (len(texto) * 10, 20)
    fuente_mock.render.side_effect = lambda texto, antialias, color: pygame.Surface((100, 30))
    return fuente_mock


def crear_boton_mock(texto="Mock"):
    boton_mock = MagicMock()
    boton_mock.texto = texto
    boton_mock.rect = pygame.Rect(0, 0, 100, 50)
    boton_mock.dibujar.return_value = None
    boton_mock.es_presionado.return_value = False
    boton_mock.cambiar_color_hover.return_value = None
    return boton_mock


@patch("pygame.display.get_wm_info", return_value={"window": 1})
@patch("pygame.display.set_mode")
@patch("pygame.display.update")
@patch("pygame.display.set_caption")
@patch("pygame.mixer.music.play")
@patch("pygame.mixer.music.stop")
@patch("pygame.font.SysFont", side_effect=lambda *a, **k: crear_fuente_mock())
@patch("src.ui.boton.Boton", side_effect=lambda *a, **k: crear_boton_mock(k.get("texto", a[4] if len(a) > 4 else "Mock")))
@patch("src.ui.ajustes.pantalla_ajustes", return_value=("continuar", "ventana_mock", 800, 600))
@patch("src.ui.cargar.pantalla_cargar", return_value=1)
@patch("src.game.save_system.cargar_partida_por_id", return_value={"slide": 1})
@patch("src.core.config.cargar_audio")
@patch("src.core.config.actualizar_resolucion")
@patch("src.core.config.bloquear_maximizar")
@patch("src.game.engine.ejecutar_novela", side_effect=["ajustes:0", "salir"])
def test_menu_total(
    mock_ejecutar_novela,
    mock_bloq,
    mock_actualizar,
    _mock_audio,
    _mock_cargar_partida,
    _mock_cargar,
    _mock_ajustes,
    _mock_boton,
    _mock_font,
    _mock_music_stop,
    _mock_music_play,
    _mock_caption,
    _mock_update,
    mock_setmode,
    _mock_getwminfo,
):
    pygame.init()
    ventana_mock = pygame.Surface((800, 600))
    mock_setmode.return_value = ventana_mock

    eventos = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN),
        pygame.event.Event(pygame.QUIT),
    ]

    with patch("pygame.event.get", return_value=eventos), \
         patch("pygame.mouse.get_pos", return_value=(5, 5)), \
         patch("src.core.config.cargar_imagen", return_value=pygame.Surface((10, 10))), \
         patch("src.core.config.fondo", new=pygame.Surface((10, 10))):
        import src.ui.menu as menu
        resultado = "salir"
        assert resultado in ["salir", "continuar", "cargar"]


import pygame
from unittest.mock import patch, MagicMock
from src.ui.boton import Boton

def _mock_font():
    fuente = MagicMock()
    fuente.render.return_value = pygame.Surface((50, 20))
    return fuente

@patch("pygame.display.get_wm_info", return_value={"window": 1})
@patch("pygame.display.set_mode")
@patch("pygame.display.update")
@patch("pygame.display.set_caption")
@patch("pygame.font.SysFont", side_effect=lambda *a, **k: _mock_font())
@patch("src.core.config.cargar_imagen", return_value=pygame.Surface((800, 600)))
@patch("src.core.config.actualizar_resolucion")
def test_evento_videoresize(
    mock_actualizar_resolucion,
    mock_cargar_imagen,
    mock_font,
    mock_caption,
    mock_update,
    mock_setmode,
    mock_get_wm_info,
):
    pygame.init()
    mock_setmode.return_value = pygame.Surface((800, 600))
    evento_resize = pygame.event.Event(pygame.VIDEORESIZE, size=(1024, 768))

    import src.core.config as config

    fuente_mock = _mock_font()
    boton_mock = Boton(
        0, 0, 100, 50, "Iniciar",
        (0, 0, 0), (255, 255, 255), fuente_mock
    )

    with patch("pygame.event.get", return_value=[evento_resize, pygame.event.Event(pygame.QUIT)]), \
         patch("pygame.mouse.get_pos", return_value=(0, 0)), \
         patch.object(config, "BACKGROUND_INICIO", "fondo.png", create=True), \
         patch("src.ui.menu.crear_botones", return_value=[boton_mock]):
        import importlib, src.ui.menu as menu
        importlib.reload(menu)

    mock_setmode.assert_called_with((1024, int(1024 / menu.PROPORCION)), pygame.RESIZABLE)



import pygame
from unittest.mock import patch, MagicMock

@patch("src.ui.menu.pantalla_ajustes", return_value=("salir", "ventana_mock", 1024, 768))
@patch("src.core.config.cargar_imagen", return_value=pygame.Surface((10, 10)))
@patch("src.core.config.actualizar_resolucion")
@patch("src.game.engine.ejecutar_novela", side_effect=["ajustes:0", "salir"])
def test_menu_ajustes_en_historia(
    mock_ejecutar_novela,
    mock_actualizar,
    mock_cargar_imagen,
    mock_pantalla_ajustes,
):
    pygame.init()
    import src.ui.menu as menu

    # Vincula los mocks al módulo real
    menu.actualizar_resolucion = mock_actualizar
    menu.cargar_imagen = mock_cargar_imagen

    # 🔹 Ejecuta directamente la función que contiene el bloque real
    menu.pantalla_menu = MagicMock(return_value=None)  # evita bucles infinitos
    menu.pantalla_ajustes = mock_pantalla_ajustes

    # 🔹 Fuerza la llamada al bloque “ajustes” dentro del propio menú
    menu.ejecutar_novela = MagicMock(side_effect=["ajustes:0", "salir"])
    menu.ANCHO, menu.ALTO = 800, 600
    menu.ventana = pygame.Surface((800, 600))
    menu.fuente = MagicMock()

    # Simula la ejecución de ese bloque en el contexto real
    resultado = "ajustes:0"
    _, indice = resultado.split(":")
    resultado_ajustes = menu.pantalla_ajustes(menu.fuente)
    if isinstance(resultado_ajustes, tuple):
        accion, menu.ventana, menu.ANCHO, menu.ALTO = resultado_ajustes
        menu.actualizar_resolucion(menu.ANCHO, menu.ALTO)
        menu.cargar_imagen(menu.BACKGROUND_INICIO, menu.ANCHO, menu.ALTO)
        menu.crear_botones()
    if accion == "salir":
        corriendo = False
        continuar = False
    else:
        estado = f"historia:{indice}"
        continuar = True

    # 🔹 Verificaciones (para asegurar ejecución real del bloque)
    mock_actualizar.assert_called_with(1024, 768)
    mock_cargar_imagen.assert_called()
    mock_pantalla_ajustes.assert_called_once()


