import pygame
from boton import Boton
from config import ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION, ALTO_BASE, CREMA, AZUL, BLANCO, AZUL_OSCURO, AZUL_RESALTADO, actualizar_resolucion, cargar_imagen, cargar_audio, bloquear_maximizar


# ===============================
# FUNCIÓN DE AJUSTES
# ===============================
def pantalla_ajustes(fuente):
    global ventana, fondo, ANCHO, ALTO
    ajustes_activo = True
    volumen = pygame.mixer.music.get_volume()
    pantalla_completa = False
    
    boton_volumen_mas = Boton(230, 250, 60, 50, "+", CREMA, AZUL, fuente)
    boton_volumen_menos = Boton(510, 250, 60, 50, "-", CREMA, AZUL, fuente)
    boton_pantalla = Boton(220, 320, 360, 60, "Pantalla Completa: OFF", CREMA, AZUL, fuente)
    boton_volver = Boton(290, 390, 220, 50, "Volver", CREMA, AZUL, fuente)
    botones_ajustes = [boton_volumen_mas, boton_volumen_menos, boton_pantalla, boton_volver]

    if ventana is None:
        ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    
    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)


    # ===============================
    # BUCLE DE AJUSTES
    # ===============================
    while ajustes_activo:
        for evento in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if evento.type == pygame.QUIT:
                ajustes_activo = False
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volumen_mas.es_click(evento.pos):
                    volumen = min(1.0, volumen + 0.1)
                    pygame.mixer.music.set_volume(volumen)
                if boton_volumen_menos.es_click(evento.pos):
                    volumen = max(0.0, volumen - 0.1)
                    pygame.mixer.music.set_volume(volumen)
                if boton_pantalla.es_click(evento.pos):
                    pantalla_completa = not pantalla_completa
                    if pantalla_completa:
                        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        info = pygame.display.Info()
                        ANCHO, ALTO = info.current_w, info.current_h
                        actualizar_resolucion(ANCHO, ALTO)
                        boton_pantalla.texto = "Pantalla Completa: ON"
                    else:
                        ANCHO = ANCHO_BASE
                        ALTO = ALTO_BASE
                        ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                        actualizar_resolucion(ANCHO, ALTO)
                        boton_pantalla.texto = "Pantalla Completa: OFF"
                    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO) 
                if boton_volver.es_click(evento.pos):
                    ajustes_activo = False
                    return "volver"

        # ===============================
        # ACTUALIZACIÓN DE PANTALLA
        # ===============================
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        ventana.blit(fondo, (0, 0))

        texto_volumen = fuente.render(f"Volumen: {int(volumen*100)}%", True, BLANCO)
        ventana.blit(texto_volumen, (ANCHO//2 - texto_volumen.get_width()//2, int(250 * escala_y)))

        for b in botones_ajustes:
            b.actualizar_posicion(escala_x, escala_y)
            b.dibujar2(ventana)

        pygame.display.update()
