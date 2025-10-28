import os
import pygame
import ctypes

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def cargar_imagen(nombre, ancho=None, alto=None):
    ruta = os.path.join(BASE_DIR, "assets", "images", nombre)
    imagen = pygame.image.load(ruta)
    if ancho and alto:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return imagen

def cargar_audio(nombre_archivo):
    ruta = os.path.join(BASE_DIR, "assets", "audio", nombre_archivo)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(ruta)
    return ruta

def bloquear_maximizar():
    if os.name == 'nt':
        hwnd = pygame.display.get_wm_info()["window"]
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style & ~0x10000)

# ===============================
# VARIABLES Y RESOLUCIÓN
# ===============================

PANTALLA_COMPLETA = False
fondo = None
PROPORCION = 1920 / 1080
ANCHO_BASE = 800
ALTO_BASE = 450
ANCHO = ANCHO_BASE
ALTO = ALTO_BASE

def actualizar_resolucion(nuevo_ancho, nuevo_alto):
    global ANCHO, ALTO
    ANCHO = nuevo_ancho
    ALTO = nuevo_alto

# ===============================
# COLORES Y PANTALLA
# ===============================

NEGRO = (0, 0, 0)
CREMA = (255, 239, 184)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
AZUL_OSCURO = (70, 110, 220)
AZUL_RESALTADO = (150, 180, 255)

ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

background_inicio = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
background_juego = cargar_imagen("background_juego.jpg", ANCHO, ALTO)
