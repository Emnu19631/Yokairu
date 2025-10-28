import pygame
from ui.boton import Boton
from core.config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION,
    ALTO_BASE, CREMA, AZUL, BLANCO, PANTALLA_COMPLETA,
    actualizar_resolucion, cargar_imagen
)

# ===============================
# FUNCIONES PRINCIPALES
# ===============================

def manejar_evento_click(evento, botones, volumen, pantalla_completa):
    global ventana, fondo, ANCHO, ALTO, PANTALLA_COMPLETA
    boton_volumen_mas, boton_volumen_menos, boton_pantalla, boton_volver = botones

    if boton_volumen_mas.es_click(evento.pos):
        volumen = min(1.0, volumen + 0.1)
        pygame.mixer.music.set_volume(volumen)
    elif boton_volumen_menos.es_click(evento.pos):
        volumen = max(0.0, volumen - 0.1)
        pygame.mixer.music.set_volume(volumen)
    elif boton_pantalla.es_click(evento.pos):
        pantalla_completa = not pantalla_completa
        PANTALLA_COMPLETA = pantalla_completa
        if pantalla_completa:
            ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            ANCHO, ALTO = info.current_w, info.current_h
            boton_pantalla.texto = "Pantalla Completa: ON"
        else:
            ANCHO, ALTO = ANCHO_BASE, ALTO_BASE
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            boton_pantalla.texto = "Pantalla Completa: OFF"
        actualizar_resolucion(ANCHO, ALTO)
        fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
    elif boton_volver.es_click(evento.pos):
        return "volver", ventana, ANCHO, ALTO, volumen, pantalla_completa

    return None, ventana, ANCHO, ALTO, volumen, pantalla_completa


def dibujar_pantalla(volumen, escala_x, escala_y, botones):
    global ventana, fondo, ANCHO, ALTO
    ventana.blit(fondo, (0, 0))
    tamano_fuente_general = int(38 * escala_y)
    tamano_fuente_botones = int(30 * escala_y)
    fuente_general = pygame.font.SysFont("Arial", tamano_fuente_general, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", tamano_fuente_botones, bold=True)

    for boton in botones:
        boton.actualizar_posicion(escala_x, escala_y)
        boton.fuente = fuente_botones
        boton.dibujar2(ventana)

    texto_volumen = fuente_general.render(f"Volumen: {int(volumen * 100)}%", True, BLANCO)
    pos_x = ANCHO // 2 - texto_volumen.get_width() // 2
    pos_y = int(180 * escala_y)
    ventana.blit(texto_volumen, (pos_x, pos_y))
    pygame.display.update()


def pantalla_ajustes(fuente):
    global ventana, fondo, ANCHO, ALTO, PANTALLA_COMPLETA
    ajustes_activo = True
    volumen = pygame.mixer.music.get_volume()
    pantalla_completa = PANTALLA_COMPLETA
    centro_x = ANCHO_BASE // 2

    boton_volumen_mas = Boton(centro_x + 150, 170, 60, 50, "+", CREMA, AZUL, fuente)
    boton_volumen_menos = Boton(centro_x - 200, 170, 60, 50, "-", CREMA, AZUL, fuente)
    texto_pantalla = "Pantalla Completa: ON" if pantalla_completa else "Pantalla Completa: OFF"
    boton_pantalla = Boton(centro_x - 180, 320, 360, 60, texto_pantalla, CREMA, AZUL, fuente)
    boton_volver = Boton(centro_x - 110, 390, 220, 50, "Volver", CREMA, AZUL, fuente)
    botones = [boton_volumen_mas, boton_volumen_menos, boton_pantalla, boton_volver]
    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

    while ajustes_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ajustes_activo = False
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                resultado, ventana, ANCHO, ALTO, volumen, pantalla_completa = manejar_evento_click(
                    evento, botones, volumen, pantalla_completa
                )
                if resultado == "volver":
                    ajustes_activo = False
                    return resultado, ventana, ANCHO, ALTO
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        dibujar_pantalla(volumen, escala_x, escala_y, botones)
