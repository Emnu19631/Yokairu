import os
import pygame
import ctypes

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BASE_DIR = os.path.dirname(__file__)  # Obtiene la ruta base del proyecto

# Carga una imagen desde el directorio 'assets/images', escalándola si es necesario
def cargar_imagen(nombre, ancho=None, alto=None):
    ruta = os.path.join(BASE_DIR, "..", "assets", "images", nombre)
    imagen = pygame.image.load(ruta)
    if ancho and alto:  # Escala la imagen si se proporcionan dimensiones
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return imagen

# Carga un archivo de audio desde el directorio 'assets/audio'
def cargar_audio(nombre_archivo):
    ruta = os.path.join(BASE_DIR, "..", "assets", "audio", nombre_archivo)
    if not pygame.mixer.get_init():  # Inicializa el mezclador de audio si no lo está
        pygame.mixer.init()
    pygame.mixer.music.load(ruta)  # Carga el archivo de audio
    return ruta

# Bloquea la opción de maximizar la ventana en sistemas Windows
def bloquear_maximizar():
    if os.name == 'nt':  # Solo en sistemas Windows
        hwnd = pygame.display.get_wm_info()["window"]
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style & ~0x10000)


# ===============================
# VARIABLES Y RESOLUCIÓN
# ===============================

fondo = None  # Fondo de la pantalla
PROPORCION = 1920 / 1080  # Relación de aspecto 16:9
ANCHO_BASE = 800  # Resolución base
ALTO_BASE = 450  # Resolución base
ANCHO = ANCHO_BASE  # Ancho de la ventana actual
ALTO = ALTO_BASE  # Alto de la ventana actual

# Actualiza la resolución de la ventana
def actualizar_resolucion(nuevo_ancho, nuevo_alto):
    global ANCHO, ALTO
    ANCHO = nuevo_ancho
    ALTO = nuevo_alto


# ===============================
# COLORES Y PANTALLA
# ===============================

# Definición de colores (en formato RGB)
CREMA = (255, 239, 184)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
AZUL_OSCURO = (70, 110, 220)
AZUL_RESALTADO = (150, 180, 255)

# Configura la ventana con la resolución actual
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)  # Carga el fondo para la ventana
