import pytest
from game.historia import HISTORIA

def test_historia_no_vacia():
    assert len(HISTORIA) > 0, "La historia no debe estar vacía."

def test_estructura_basica_historia():
    for i, slide in enumerate(HISTORIA):
        assert isinstance(slide, dict), f"El elemento {i} no es un diccionario."
        assert "tipo" in slide, f"El elemento {i} no tiene clave 'tipo'."
        assert slide["tipo"] in ["narracion", "eleccion"], f"Tipo inválido en slide {i}."

def test_referencias_de_next_validas():
    total_slides = len(HISTORIA)
    for i, slide in enumerate(HISTORIA):
        if "opciones" in slide:
            for op in slide["opciones"]:
                next_id = op.get("next")
                if next_id is not None:
                    assert 0 <= next_id < total_slides, f"Referencia 'next' inválida en slide {i}"
