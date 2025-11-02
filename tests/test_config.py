from core import config
import pygame
import os

def test_cargar_imagen_existe():
    assert callable(config.cargar_imagen)

def test_actualizar_resolucion():
    config.actualizar_resolucion(1280, 720)
    assert config.ANCHO == 1280
    assert config.ALTO == 720

def test_cargar_audio_existe(tmp_path):
    fake_audio = tmp_path / "test_audio.mp3"
    fake_audio.write_text("fake")
    ruta = str(fake_audio)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    pygame.mixer.quit()
    try:
        config.cargar_audio(os.path.basename(ruta))
    except Exception:
        pass
    assert callable(config.cargar_audio)

def test_bloquear_maximizar_existe(monkeypatch):
    if os.name == "nt":
        monkeypatch.setattr(pygame.display, "get_wm_info", lambda: {"window": 123})
        monkeypatch.setattr(config.ctypes.windll.user32, "GetWindowLongPtrW", lambda *a: 1)
        monkeypatch.setattr(config.ctypes.windll.user32, "SetWindowLongPtrW", lambda *a: None)
    config.bloquear_maximizar()
    assert callable(config.bloquear_maximizar)
