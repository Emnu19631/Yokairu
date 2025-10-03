import pygame
import os
import ctypes

def bloquear_maximizar():
    if os.name == 'nt':
        hwnd = pygame.display.get_wm_info()["window"]
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style & ~0x10000)

pygame.init()

ANCHO_IMAGEN = 1920
ALTO_IMAGEN = 1080
PROPORCION = ANCHO_IMAGEN / ALTO_IMAGEN

ANCHO = 800
ALTO = int(ANCHO / PROPORCION)

ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("YOKAIRYU")

bloquear_maximizar()

NEGRO = (0, 0, 0)

fondo = pygame.image.load('C:/Users/Adrian/Documents/calidad/proyecto/images/background_inicio.jpg')
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

pygame.mixer.music.load('C:/Users/Adrian/Documents/calidad/proyecto/audio/background_audio.mp3')
pygame.mixer.music.play(-1, 0.0)

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.VIDEORESIZE:
            ANCHO, ALTO = evento.size
            ALTO = int(ANCHO / PROPORCION)
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    ventana.blit(fondo, (0, 0))
    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
