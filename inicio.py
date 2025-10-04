import pygame
import os
import ctypes

BASE_DIR = os.path.dirname(__file__)

def cargar_imagen(nombre, ancho=None, alto=None):
    ruta = os.path.join(BASE_DIR, "images", nombre)
    imagen = pygame.image.load(ruta)
    if ancho and alto:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return imagen

def cargar_audio(nombre):
    ruta = os.path.join(BASE_DIR, "audio", nombre)
    pygame.mixer.music.load(ruta)
    return ruta

def bloquear_maximizar():
    if os.name == 'nt':
        hwnd = pygame.display.get_wm_info()["window"]
        style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -16)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -16, style & ~0x10000)

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_fondo, color_texto, fuente,
                 color_hover=None, color_seleccion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.fuente = fuente
        self.color_hover = color_hover if color_hover else color_fondo
        self.color_seleccion = color_seleccion if color_seleccion else (200, 220, 255)

    def dibujar(self, ventana, mouse_pos, seleccionado=False):
        # Color según estado
        if seleccionado:
            color = self.color_seleccion
        elif self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_fondo

        pygame.draw.rect(ventana, color, self.rect, border_radius=20)
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        ventana.blit(
            texto_render,
            (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,
             self.rect.y + (self.rect.height - texto_render.get_height()) // 2)
        )

    def es_click(self, pos):
        return self.rect.collidepoint(pos)


pygame.init()

ANCHO_IMAGEN = 1920
ALTO_IMAGEN = 1080
PROPORCION = ANCHO_IMAGEN / ALTO_IMAGEN

ANCHO = 800
ALTO = int(ANCHO / PROPORCION)

ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("YOKAIRYU")

bloquear_maximizar()

CREMA = (255, 240, 200)
AZUL = (100, 150, 255)
AZUL_OSCURO = (70, 110, 220)
AZUL_RESALTADO = (150, 180, 255)

fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

cargar_audio("background_audio.mp3")
pygame.mixer.music.play(-1, 0.0)

fuente = pygame.font.SysFont("Arial", 38, bold=True)

boton_ancho = 220
boton_alto = 50
espaciado = 15
inicio_y = 180
botones_textos = ["Iniciar", "Tutorial", "Créditos", "Salir"]

botones = []
for i, texto in enumerate(botones_textos):
    x = ANCHO // 2 - boton_ancho // 2
    y = inicio_y + i * (boton_alto + espaciado)
    botones.append(
        Boton(x, y, boton_ancho, boton_alto, texto, CREMA, AZUL, fuente,
              color_hover=AZUL_OSCURO, color_seleccion=AZUL_RESALTADO)
    )

def iniciar_partida(ventana, ancho, alto, fuente):
    """Escena temporal de iniciar partida"""
    ventana.fill((30, 60, 120))
    texto = "Se está trabajando en esta función..."
    texto_render = fuente.render(texto, True, (255, 240, 200))
    ventana.blit(
        texto_render,
        ((ancho - texto_render.get_width()) // 2,
         (alto - texto_render.get_height()) // 2)
    )
    pygame.display.update()
    pygame.time.wait(2000)

# 🔹 Índice del botón actualmente seleccionado
indice_seleccionado = 0

corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        elif evento.type == pygame.VIDEORESIZE:
            ANCHO, ALTO = evento.size
            ALTO = int(ANCHO / PROPORCION)
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

        elif evento.type == pygame.KEYDOWN:
            # Navegación con flechas
            if evento.key in (pygame.K_UP, pygame.K_LEFT):
                indice_seleccionado = (indice_seleccionado - 1) % len(botones)
            elif evento.key in (pygame.K_DOWN, pygame.K_RIGHT):
                indice_seleccionado = (indice_seleccionado + 1) % len(botones)
            # Activar con Enter o Espacio
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                texto = botones[indice_seleccionado].texto
                print(f"Botón {texto} activado")
                if texto == "Salir":
                    corriendo = False
                elif texto == "Iniciar":
                    iniciar_partida(ventana, ANCHO, ALTO, fuente)

        elif evento.type == pygame.MOUSEMOTION:
            # Si el mouse pasa por encima, actualiza la selección
            for i, boton in enumerate(botones):
                if boton.rect.collidepoint(evento.pos):
                    indice_seleccionado = i
                    break

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                for i, boton in enumerate(botones):
                    if boton.es_click(evento.pos):
                        indice_seleccionado = i
                        texto = boton.texto
                        print(f"Botón {texto} presionado")
                        if texto == "Salir":
                            corriendo = False
                        elif texto == "Iniciar":
                            iniciar_partida(ventana, ANCHO, ALTO, fuente)

    ventana.blit(fondo, (0, 0))

    # 🔹 Dibujar todos los botones
    for i, boton in enumerate(botones):
        boton.dibujar(ventana, mouse_pos, seleccionado=(i == indice_seleccionado))

    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
