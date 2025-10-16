import pygame
import sys
from guardar import guardar_partida, cargar_partida
from iniciar_partida import iniciar_partida
from boton import Boton
from config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION, ALTO_BASE,
    CREMA, AZUL, BLANCO, AZUL_OSCURO, AZUL_RESALTADO,
    actualizar_resolucion, cargar_imagen, cargar_audio, bloquear_maximizar
)
from ajustes import pantalla_ajustes

# ===============================
# INICIALIZACIÓN DE PYGAME
# ===============================
pygame.init()
fuente = pygame.font.SysFont("Arial", 38, bold=True)
pygame.display.set_caption("YOKAIRYU")
bloquear_maximizar()

cargar_audio("background_audio.mp3")
pygame.mixer.music.play(-1, 0.0)

# ===============================
# CONFIGURACIÓN DE BOTONES
# ===============================
boton_ancho = 180
boton_alto = 35
espaciado = 15
inicio_y_base = 200  # posición base del primer botón

botones_textos = ["Iniciar", "Cargar", "Ajustes", "Salir"]
botones = []

def crear_botones():
    """Recrea los botones según el tamaño actual de la ventana."""
    nuevos_botones = []
    escala_x = ANCHO / ANCHO_BASE
    escala_y = ALTO / ALTO_BASE
    
    for i, texto in enumerate(botones_textos):
        x = int(ANCHO_BASE // 2 - boton_ancho // 2)
        y = int(inicio_y_base + i * (boton_alto + espaciado))
        nuevo_boton = Boton(x, y, boton_ancho, boton_alto, texto, CREMA, AZUL, fuente)
        nuevo_boton.actualizar_posicion(escala_x, escala_y)
        nuevos_botones.append(nuevo_boton)
    return nuevos_botones

botones = crear_botones()

# ===============================
# BUCLE PRINCIPAL DEL JUEGO
# ===============================
indice_seleccionado = 0
corriendo = True

while corriendo:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        elif evento.type == pygame.VIDEORESIZE:
            # Ajustar resolución dinámica
            ANCHO, ALTO = evento.size
            ALTO = int(ANCHO / PROPORCION)
            actualizar_resolucion(ANCHO, ALTO)
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
            botones = crear_botones()

        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_LEFT):
                indice_seleccionado = (indice_seleccionado - 1) % len(botones)
            elif evento.key in (pygame.K_DOWN, pygame.K_RIGHT):
                indice_seleccionado = (indice_seleccionado + 1) % len(botones)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                texto = botones[indice_seleccionado].texto
                print(f"Botón {texto} activado")

                if texto == "Salir":
                    corriendo = False

                elif texto == "Iniciar":
                    iniciar_partida(ventana, ANCHO, ALTO, fuente)

                elif texto == "Ajustes":
                    resultado = pantalla_ajustes(fuente)
                    if isinstance(resultado, tuple):
                        accion, ventana, ANCHO, ALTO = resultado
                        actualizar_resolucion(ANCHO, ALTO)
                        fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
                        botones = crear_botones()
                    else:
                        accion = resultado
                    if accion == "salir":
                        corriendo = False

        elif evento.type == pygame.MOUSEMOTION:
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

                        elif texto == "Ajustes":
                            resultado = pantalla_ajustes(fuente)
                            if isinstance(resultado, tuple):
                                accion, ventana, ANCHO, ALTO = resultado
                                actualizar_resolucion(ANCHO, ALTO)
                                fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
                                botones = crear_botones()
                            else:
                                accion = resultado
                            if accion == "salir":
                                corriendo = False

    # ===============================
    # DIBUJO DE INTERFAZ
    # ===============================
    ventana.blit(fondo, (0, 0))

    for i, boton in enumerate(botones):
        boton.dibujar(ventana, mouse_pos, seleccionado=(i == indice_seleccionado))

    pygame.display.update()

# ===============================
# FINALIZACIÓN DEL JUEGO
# ===============================
pygame.mixer.music.stop()
pygame.quit()
