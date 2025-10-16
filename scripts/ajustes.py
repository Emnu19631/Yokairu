import pygame
from boton import Boton
from config import ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION, ALTO_BASE, CREMA, AZUL, BLANCO, actualizar_resolucion, cargar_imagen


def pantalla_ajustes(fuente):
    global ventana, fondo, ANCHO, ALTO
    ajustes_activo = True
    volumen = pygame.mixer.music.get_volume()

    # 🔧 Detectar si ya está en pantalla completa
    fullscreen_actual = ventana.get_flags() & pygame.FULLSCREEN
    pantalla_completa = bool(fullscreen_actual)
    
    # Calcular posiciones base centradas
    centro_x = ANCHO_BASE // 2
    
    # Botones de volumen
    boton_volumen_mas = Boton(centro_x + 100, 250, 60, 50, "+", CREMA, AZUL, fuente)
    boton_volumen_menos = Boton(centro_x - 160, 250, 60, 50, "-", CREMA, AZUL, fuente)
    
    # Botón de pantalla completa
    texto_pantalla = "Pantalla Completa: ON" if pantalla_completa else "Pantalla Completa: OFF"
    boton_pantalla = Boton(centro_x - 180, 320, 360, 60, texto_pantalla, CREMA, AZUL, fuente)
    
    # Botón volver
    boton_volver = Boton(centro_x - 110, 390, 220, 50, "Volver", CREMA, AZUL, fuente)
    
    botones_ajustes = [boton_volumen_mas, boton_volumen_menos, boton_pantalla, boton_volver]

    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

    while ajustes_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ajustes_activo = False
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volumen_mas.es_click(evento.pos):
                    volumen = min(1.0, volumen + 0.1)
                    pygame.mixer.music.set_volume(volumen)
                elif boton_volumen_menos.es_click(evento.pos):
                    volumen = max(0.0, volumen - 0.1)
                    pygame.mixer.music.set_volume(volumen)
                elif boton_pantalla.es_click(evento.pos):
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
                elif boton_volver.es_click(evento.pos):
                    # 🔧 Al volver, conserva el modo actual (pantalla completa o ventana)
                    if pantalla_completa:
                        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        info = pygame.display.Info()
                        ANCHO, ALTO = info.current_w, info.current_h
                    else:
                        ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
                    pygame.display.update()
                    ajustes_activo = False
                    return "volver", ventana, ANCHO, ALTO

        # ===============================
        # DIBUJO
        # ===============================
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        ventana.blit(fondo, (0, 0))

        texto_volumen = fuente.render(f"Volumen: {int(volumen * 100)}%", True, BLANCO)
        ventana.blit(texto_volumen, (ANCHO // 2 - texto_volumen.get_width() // 2, int(250 * escala_y)))

        for b in botones_ajustes:
            b.actualizar_posicion(escala_x, escala_y)
            b.dibujar2(ventana)

        pygame.display.update()
