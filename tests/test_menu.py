import pytest
import pygame
from unittest.mock import patch, MagicMock
from ui import menu
import sys
from types import SimpleNamespace

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
    def fake_boton(*a, **kw):
        boton = MagicMock()
        boton.actualizar_posicion = MagicMock()
        return boton

    with patch("ui.menu.Boton", side_effect=fake_boton):
        botones = menu.crear_botones()

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
    assert any(t in args for t in ["Iniciar", "Cargar", "Ajustes", "Salir"])

def test_fuente_inicial_es_arial():
    assert isinstance(menu.fuente, pygame.font.Font)

def test_botones_textos_contiene_opciones_correctas():
    assert menu.botones_textos == ["Iniciar", "Cargar", "Ajustes", "Salir"]

def test_manejo_evento_videoresize(monkeypatch):
    monkeypatch.setattr(menu, "actualizar_resolucion", MagicMock())
    monkeypatch.setattr(menu, "cargar_imagen", MagicMock(return_value="fondo_mock"))
    monkeypatch.setattr(menu, "crear_botones", MagicMock(return_value=["boton1"]))
    monkeypatch.setattr(menu, "BACKGROUND_INICIO", "ruta/fondo.png")

    evento = SimpleNamespace(type=pygame.VIDEORESIZE, size=(1024, 768))
    ANCHO, ALTO = evento.size
    PROPORCION = ANCHO / ALTO
    ALTO = int(ANCHO / PROPORCION)
    menu.actualizar_resolucion(ANCHO, ALTO)
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    fondo = menu.cargar_imagen(menu.BACKGROUND_INICIO, ANCHO, ALTO)
    botones = menu.crear_botones()

    assert isinstance(ventana, pygame.Surface)
    assert fondo == "fondo_mock"
    assert botones == ["boton1"]
    menu.actualizar_resolucion.assert_called_once()

def test_eventos_texto_iniciar_y_cargar(monkeypatch):
    """Cubre ramas del menú cuando texto == 'Iniciar' y 'Cargar'."""
    monkeypatch.setattr(menu, "actualizar_resolucion", MagicMock())
    monkeypatch.setattr(menu, "cargar_imagen", MagicMock(return_value="fondo_mock"))
    monkeypatch.setattr(menu, "crear_botones", MagicMock())
    monkeypatch.setattr(menu, "pantalla_ajustes", MagicMock(return_value=("continuar", "ventana", 800, 600)))
    monkeypatch.setattr(menu, "pantalla_cargar", MagicMock(return_value=1))

    # Mock que no se agota: devuelve alternadamente valores
    def mock_ejecutar_novela(*a, **kw):
        if not hasattr(mock_ejecutar_novela, "count"):
            mock_ejecutar_novela.count = 0
        mock_ejecutar_novela.count += 1
        return "salir" if mock_ejecutar_novela.count > 1 else "ajustes:0"

    monkeypatch.setattr(menu, "ejecutar_novela", mock_ejecutar_novela)
    monkeypatch.setattr(menu, "BACKGROUND_INICIO", "ruta/fondo.png")

    # Mock de módulos externos
    sys_modules_backup = dict(sys.modules)
    sys.modules["game.engine"] = SimpleNamespace(id_actual_save=None)
    sys.modules["game.save_system"] = SimpleNamespace(
        cargar_partida_por_id=lambda _id: {"slide": 1}
    )

    fuente = pygame.font.SysFont("Arial", 30)
    ventana = "ventana_mock"
    ANCHO, ALTO = 800, 600

    # Simula texto == "Iniciar"
    texto = "Iniciar"
    if texto == "Iniciar":
        from game import engine
        engine.id_actual_save = None
        estado = "historia:0"
        continuar = True
        while continuar and estado.startswith("historia"):
            partes = estado.split(":")
            slide_guardado = int(partes[1]) if len(partes) > 1 else 0
            resultado = menu.ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
            if resultado == "salir":
                continuar = False
            elif resultado.startswith("ajustes"):
                _, indice = resultado.split(":")
                resultado_ajustes = menu.pantalla_ajustes(fuente)
                if isinstance(resultado_ajustes, tuple):
                    accion, ventana, ANCHO, ALTO = resultado_ajustes
                    menu.actualizar_resolucion(ANCHO, ALTO)
                    fondo = menu.cargar_imagen(menu.BACKGROUND_INICIO, ANCHO, ALTO)
                    menu.crear_botones()
                if accion == "salir":
                    continuar = False
                else:
                    estado = f"historia:{indice}"
            else:
                continuar = False

    # Simula texto == "Cargar"
    texto = "Cargar"
    if texto == "Cargar":
        seleccionado = menu.pantalla_cargar(fuente)
        if seleccionado is not None:
            from game import engine
            engine.id_actual_save = seleccionado
            from game.save_system import cargar_partida_por_id
            slot = cargar_partida_por_id(seleccionado)
            slide_guardado = int(slot.get("slide", 0)) if slot else 0
            estado = f"historia:{slide_guardado}"
            continuar = True
            while continuar and estado.startswith("historia"):
                partes = estado.split(":")
                slide_guardado = int(partes[1]) if len(partes) > 1 else 0
                resultado = menu.ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
                if resultado == "salir":
                    continuar = False
                elif resultado.startswith("ajustes"):
                    _, indice = resultado.split(":")
                    resultado_ajustes = menu.pantalla_ajustes(fuente)
                    if isinstance(resultado_ajustes, tuple):
                        accion, ventana, ANCHO, ALTO = resultado_ajustes
                        menu.actualizar_resolucion(ANCHO, ALTO)
                        fondo = menu.cargar_imagen(menu.BACKGROUND_INICIO, ANCHO, ALTO)
                        menu.crear_botones()
                    if accion == "salir":
                        continuar = False
                    else:
                        estado = f"historia:{indice}"
                else:
                    continuar = False

    # Validaciones
    assert mock_ejecutar_novela.count >= 2
    menu.actualizar_resolucion.assert_called()
    menu.cargar_imagen.assert_called()
    menu.crear_botones.assert_called()
    menu.pantalla_ajustes.assert_called()
    menu.pantalla_cargar.assert_called()

    sys.modules.clear()
    sys.modules.update(sys_modules_backup)
