import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from game import save_system


# =======================================================
# TESTS DE FUNCIONES PRIVADAS (_leer_todos y _escribir_todos)
# =======================================================

def test__leer_todos_devuelve_lista_correcta(monkeypatch):
    fake_data = [{"id": 1, "slide": 3}]
    mock_file = mock_open(read_data=json.dumps(fake_data))
    monkeypatch.setattr("os.path.exists", lambda x: True)

    with patch("builtins.open", mock_file):
        result = save_system._leer_todos()

    assert result == fake_data


def test__leer_todos_maneja_json_corrupto(monkeypatch):
    mock_file = mock_open(read_data="{json invalido")
    monkeypatch.setattr("os.path.exists", lambda x: True)
    with patch("builtins.open", mock_file):
        result = save_system._leer_todos()
    assert result == []


def test__leer_todos_archivo_inexistente(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda x: False)
    result = save_system._leer_todos()
    assert result == []


def test__escribir_todos_guarda_json(monkeypatch):
    mock_makedirs = MagicMock()
    mock_file = mock_open()

    monkeypatch.setattr("os.makedirs", mock_makedirs)
    with patch("builtins.open", mock_file):
        save_system._escribir_todos([{"id": 1, "slide": 3}])

    mock_makedirs.assert_called_once()
    handle = mock_file()
    handle.write.assert_called()


# =======================================================
# TESTS DE guardar_partida
# =======================================================

def test_guardar_partida_crea_nuevo(monkeypatch):
    monkeypatch.setattr(save_system, "_leer_todos", lambda: [])
    mock_escribir = MagicMock()
    monkeypatch.setattr(save_system, "_escribir_todos", mock_escribir)
    mock_datetime = datetime(2024, 1, 1, 10, 0, 0)
    monkeypatch.setattr(save_system, "datetime", MagicMock(now=lambda: mock_datetime))

    result = save_system.guardar_partida(5)

    assert result["id"] == 1
    assert result["slide"] == 5
    assert "fecha" in result
    mock_escribir.assert_called_once()


def test_guardar_partida_actualiza_existente(monkeypatch):
    existente = [{"id": 2, "slide": 10, "fecha": "2024-01-01 00:00:00"}]
    monkeypatch.setattr(save_system, "_leer_todos", lambda: existente.copy())
    mock_escribir = MagicMock()
    monkeypatch.setattr(save_system, "_escribir_todos", mock_escribir)

    mock_datetime = datetime(2024, 1, 2, 12, 0, 0)
    monkeypatch.setattr(save_system, "datetime", MagicMock(now=lambda: mock_datetime))

    result = save_system.guardar_partida(15, id_existente=2)

    assert result["slide"] == 15
    assert "2024-01-02" in result["fecha"]
    mock_escribir.assert_called_once()


def test_guardar_partida_incrementa_id(monkeypatch):
    lista = [{"id": 1, "slide": 3}, {"id": 3, "slide": 9}]
    monkeypatch.setattr(save_system, "_leer_todos", lambda: lista)
    mock_escribir = MagicMock()
    monkeypatch.setattr(save_system, "_escribir_todos", mock_escribir)

    result = save_system.guardar_partida(7)
    assert result["id"] == 4  # máximo + 1


# =======================================================
# TESTS DE listar_guardados
# =======================================================

def test_listar_guardados_ordena_por_fecha(monkeypatch):
    lista = [
        {"id": 1, "slide": 1, "fecha": "2023-01-01 00:00:00"},
        {"id": 2, "slide": 2, "fecha": "2024-01-01 00:00:00"}
    ]
    monkeypatch.setattr(save_system, "_leer_todos", lambda: lista)
    result = save_system.listar_guardados()
    assert result[0]["id"] == 2  # más reciente primero


def test_listar_guardados_maneja_error(monkeypatch):
    monkeypatch.setattr(save_system, "_leer_todos", lambda: [{"id": 1, "slide": 2, "fecha": None}])
    result = save_system.listar_guardados()
    assert isinstance(result, list)


# =======================================================
# TESTS DE cargar_partida_por_id
# =======================================================

def test_cargar_partida_por_id_encontrada(monkeypatch):
    lista = [{"id": 5, "slide": 8}]
    monkeypatch.setattr(save_system, "_leer_todos", lambda: lista)
    result = save_system.cargar_partida_por_id(5)
    assert result["slide"] == 8


def test_cargar_partida_por_id_no_encontrada(monkeypatch):
    lista = [{"id": 2, "slide": 1}]
    monkeypatch.setattr(save_system, "_leer_todos", lambda: lista)
    result = save_system.cargar_partida_por_id(10)
    assert result is None


# =======================================================
# TESTS DE hay_partida_guardada
# =======================================================

def test_hay_partida_guardada_true(monkeypatch):
    monkeypatch.setattr(save_system, "_leer_todos", lambda: [{"id": 1}])
    assert save_system.hay_partida_guardada() is True


def test_hay_partida_guardada_false(monkeypatch):
    monkeypatch.setattr(save_system, "_leer_todos", lambda: [])
    assert save_system.hay_partida_guardada() is False
