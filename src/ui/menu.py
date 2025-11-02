import pygame
import sys
from game.save_system import listar_guardados, cargar_partida_por_id
from ui.boton import Boton
from core.config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION, ALTO_BASE,
    CREMA, AZUL, BLANCO, AZUL_OSCURO, AZUL_RESALTADO, PANTALLA_COMPLETA,
    actualizar_resolucion, cargar_imagen, cargar_audio, bloquear_maximizar
)
from ui.ajustes import pantalla_ajustes
from game.engine import ejecutar_novela
from ui.cargar import pantalla_cargar


# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BACKGROUND_INICIO = "background_inicio.jpg"

if PANTALLA_COMPLETA:
    ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

# ===============================
# INICIALIZACIÓN DE PYGAME
# ===============================

pygame.init()
fuente = pygame.font.SysFont("Arial", 34, bold=True)
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
inicio_y_base = 200
botones_textos = ["Iniciar", "Cargar", "Ajustes", "Salir"]
botones = []


def crear_botones():
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
            ANCHO, ALTO = evento.size
            ALTO = int(ANCHO / PROPORCION)
            actualizar_resolucion(ANCHO, ALTO)
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
            botones = crear_botones()
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_LEFT):
                indice_seleccionado = (indice_seleccionado - 1) % len(botones)
            elif evento.key in (pygame.K_DOWN, pygame.K_RIGHT):
                indice_seleccionado = (indice_seleccionado + 1) % len(botones)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                texto = botones[indice_seleccionado].texto
                if texto == "Salir":
                    corriendo = False
                elif texto == "Iniciar":
                    estado = "historia:0"
                    continuar = True
                    while continuar and estado.startswith("historia"):
                        partes = estado.split(":")
                        slide_guardado = int(partes[1]) if len(partes) > 1 else 0
                        resultado = ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
                        if resultado == "salir":
                            corriendo = False
                            continuar = False
                        elif resultado.startswith("ajustes"):
                            _, indice = resultado.split(":")
                            resultado_ajustes = pantalla_ajustes(fuente)
                            if isinstance(resultado_ajustes, tuple):
                                accion, ventana, ANCHO, ALTO = resultado_ajustes
                                actualizar_resolucion(ANCHO, ALTO)
                                fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
                                botones = crear_botones()
                            if accion == "salir":
                                corriendo = False
                                continuar = False
                            else:
                                estado = f"historia:{indice}"
                        else:
                            continuar = False
                elif texto == "Cargar":
                    # abrir pantalla de carga (retorna slide o None)
                    seleccionado = pantalla_cargar(fuente)
                    if seleccionado is not None:
                        estado = f"historia:{seleccionado}"
                        continuar = True
                        while continuar and estado.startswith("historia"):
                            partes = estado.split(":")
                            slide_guardado = int(partes[1]) if len(partes) > 1 else 0
                            resultado = ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
                            if resultado == "salir":
                                corriendo = False
                                continuar = False
                            elif resultado.startswith("ajustes"):
                                _, indice = resultado.split(":")
                                resultado_ajustes = pantalla_ajustes(fuente)
                                if isinstance(resultado_ajustes, tuple):
                                    accion, ventana, ANCHO, ALTO = resultado_ajustes
                                    actualizar_resolucion(ANCHO, ALTO)
                                    fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
                                    botones = crear_botones()
                                if accion == "salir":
                                    corriendo = False
                                    continuar = False
                                else:
                                    estado = f"historia:{indice}"
                            else:
                                continuar = False
                elif texto == "Ajustes":
                    resultado = pantalla_ajustes(fuente)
                    if isinstance(resultado, tuple):
                        accion, ventana, ANCHO, ALTO = resultado
                        actualizar_resolucion(ANCHO, ALTO)
                        fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
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
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, boton in enumerate(botones):
                if boton.es_click(evento.pos):
                    indice_seleccionado = i
                    texto = boton.texto
                    if texto == "Salir":
                        corriendo = False
                    elif texto == "Iniciar":
                        estado = "historia:0"
                        continuar = True
                        while continuar and estado.startswith("historia"):
                            partes = estado.split(":")
                            slide_guardado = int(partes[1]) if len(partes) > 1 else 0
                            resultado = ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
                            if resultado == "salir":
                                corriendo = False
                                continuar = False
                            elif resultado.startswith("ajustes"):
                                _, indice = resultado.split(":")
                                resultado_ajustes = pantalla_ajustes(fuente)
                                if isinstance(resultado_ajustes, tuple):
                                    accion, ventana, ANCHO, ALTO = resultado_ajustes
                                    actualizar_resolucion(ANCHO, ALTO)
                                    fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
                                    botones = crear_botones()
                                if accion == "salir":
                                    corriendo = False
                                    continuar = False
                                else:
                                    estado = f"historia:{indice}"
                            else:
                                continuar = False
                    elif texto == "Cargar":
                        seleccionado = pantalla_cargar(fuente)
                        if seleccionado is not None:
                            estado = f"historia:{seleccionado}"
                            continuar = True
                            while continuar and estado.startswith("historia"):
                                partes = estado.split(":")
                                slide_guardado = int(partes[1]) if len(partes) > 1 else 0
                                resultado = ejecutar_novela(ventana, fuente, ANCHO, ALTO, slide_guardado)
                                if resultado == "salir":
                                    corriendo = False
                                    continuar = False
                                elif resultado.startswith("ajustes"):
                                    _, indice = resultado.split(":")
                                    resultado_ajustes = pantalla_ajustes(fuente)
                                    if isinstance(resultado_ajustes, tuple):
                                        accion, ventana, ANCHO, ALTO = resultado_ajustes
                                        actualizar_resolucion(ANCHO, ALTO)
                                        fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
                                        botones = crear_botones()
                                    if accion == "salir":
                                        corriendo = False
                                        continuar = False
                                    else:
                                        estado = f"historia:{indice}"
                                else:
                                    continuar = False
                    elif texto == "Ajustes":
                        resultado = pantalla_ajustes(fuente)
                        if isinstance(resultado, tuple):
                            accion, ventana, ANCHO, ALTO = resultado
                            actualizar_resolucion(ANCHO, ALTO)
                            fondo = cargar_imagen(BACKGROUND_INICIO, ANCHO, ALTO)
                            botones = crear_botones()
                        else:
                            accion = resultado
                        if accion == "salir":
                            corriendo = False

    ventana.blit(fondo, (0, 0))
    for i, boton in enumerate(botones):
        boton.dibujar(ventana, mouse_pos, seleccionado=(i == indice_seleccionado))
    pygame.display.update()

# ===============================
# FINALIZACIÓN DEL JUEGO
# ===============================

pygame.mixer.music.stop()
pygame.quit()
