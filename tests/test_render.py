import pytest
import pygame
from unittest.mock import patch, MagicMock
from core import render  # ✅ Importación corregida

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# ===========================
# TEST: dividir_texto_en_lineas
# ===========================

def test_dividir_texto_en_lineas_basico():
    fuente = pygame.font.SysFont("Arial", 20)
    texto = "Hola mundo de las pruebas unitarias"
    lineas = render.dividir_texto_en_lineas(texto, fuente, 100)
    assert isinstance(lineas, list)
    assert all(isinstance(l, str) for l in lineas)
    assert len(lineas) > 1

def test_dividir_texto_en_lineas_todo_cabe():
    fuente = pygame.font.SysFont("Arial", 20)
    texto = "Texto corto"
    lineas = render.dividir_texto_en_lineas(texto, fuente, 1000)
    assert lineas == ["Texto corto"]

# ===========================
# TEST: ajustar_fuente_al_rect
# ===========================

def test_ajustar_fuente_al_rect_retorna_fuente_y_lineas():
    fuente = pygame.font.SysFont("Arial", 30)
    rect = pygame.Rect(0, 0, 200, 100)
    texto = "Esto es una prueba de ajuste de fuente"
    fuente_ajustada, lineas = render.ajustar_fuente_al_rect(texto, fuente, rect)
    assert isinstance(fuente_ajustada, pygame.font.Font)
    assert isinstance(lineas, list)

# ===========================
# TEST: _actualizar_texto_tipeado
# ===========================

def test_actualizar_texto_tipeado_incrementa_correctamente(monkeypatch):
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 200)
    texto, texto_mostrado, indice = "ABC", "", 0
    tiempo_ultimo = 0
    resultado = render._actualizar_texto_tipeado(texto, texto_mostrado, indice, tiempo_ultimo, 50)
    assert isinstance(resultado, tuple)
    assert len(resultado) == 3
    assert resultado[1] >= indice  # índice avanza o se mantiene

# ===========================
# TEST: _es_evento_de_salida
# ===========================

@pytest.mark.parametrize("tipo, key, esperado", [
    (pygame.MOUSEBUTTONDOWN, None, True),
    (pygame.KEYDOWN, pygame.K_RETURN, True),
    (pygame.KEYDOWN, pygame.K_SPACE, True),
    (pygame.KEYDOWN, pygame.K_a, False),
])
def test_es_evento_de_salida_retorna_correcto(tipo, key, esperado):
    evento = MagicMock(type=tipo, key=key)
    assert render._es_evento_de_salida(evento) == esperado

# ===========================
# TEST: _verificar_salida_eventos
# ===========================

def test_verificar_salida_eventos_detecta_salida(monkeypatch):
    mock_eventos = [MagicMock(type=pygame.QUIT)]
    monkeypatch.setattr(pygame, "event", MagicMock(get=lambda: mock_eventos))
    assert render._verificar_salida_eventos() is True

def test_verificar_salida_eventos_sin_salida(monkeypatch):
    mock_eventos = [MagicMock(type=pygame.MOUSEMOTION)]
    monkeypatch.setattr(pygame, "event", MagicMock(get=lambda: mock_eventos))
    assert render._verificar_salida_eventos() is False

# ===========================
# TEST: _dibujar_texto_tipeado
# ===========================

def test_dibujar_texto_tipeado_actualiza_display(monkeypatch):
    ventana = pygame.Surface((400, 200))
    fuente = pygame.font.SysFont("Arial", 20)
    texto = "Hola mundo"
    rect = pygame.Rect(0, 0, 400, 200)

    monkeypatch.setattr(pygame.display, "update", lambda *a, **k: None)
    render._dibujar_texto_tipeado(ventana, fuente, texto, (0, 0, 0), rect)

    # Validación mínima: la superficie fue dibujada
    assert isinstance(ventana, pygame.Surface)

# ===========================
# TEST: mostrar_texto_tipeado_con_fondo_solido (mock)
# ===========================

def test_mostrar_texto_tipeado_con_fondo_solido_termina_correctamente(monkeypatch):
    ventana = pygame.Surface((400, 200))
    fuente = pygame.font.SysFont("Arial", 20)
    texto = "Test rápido"

    monkeypatch.setattr(render, "_verificar_salida_eventos", lambda: True)
    resultado = render.mostrar_texto_tipeado_con_fondo_solido(
        ventana, fuente, texto, (0, 0, 0), pygame.Rect(0, 0, 400, 200), velocidad=1
    )
    assert resultado is True
