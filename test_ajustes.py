import pytest
import pygame

def test_volumen():
    pygame.mixer.init()
    
    volumen_inicial = pygame.mixer.music.get_volume()
    
    pygame.mixer.music.set_volume(min(1.0, volumen_inicial + 0.1))
    assert pygame.mixer.music.get_volume() > volumen_inicial
    
    pygame.mixer.music.set_volume(max(0.0, volumen_inicial - 0.1))
    assert pygame.mixer.music.get_volume() <= volumen_inicial
