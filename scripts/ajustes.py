import pygame
from boton import Boton
from config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION,
    ALTO_BASE, CREMA, AZUL, BLANCO, actualizar_resolucion, cargar_imagen
)

def pantalla_ajustes(fuente):
    global ventana, fondo, ANCHO, ALTO
    ajustes_activo = True
    volumen = pygame.mixer.music.get_volume()

    # 🔧 Detectar si ya está en pantalla completa
    fullscreen_actual = ventana.get_flags() & pygame.FULLSCREEN
    pantalla_completa = bool(fullscreen_actual)

    # Calcular posiciones base centradas
    centro_x = ANCHO_BASE // 2

    # 🔘 Crear botones base (coordenadas relativas)
    boton_volumen_mas = Boton(centro_x + 150, 170, 60, 50, "+", CREMA, AZUL, fuente)
    boton_volumen_menos = Boton(centro_x - 200, 170, 60, 50, "-", CREMA, AZUL, fuente)

    texto_pantalla = "Pantalla Completa: ON" if pantalla_completa else "Pantalla Completa: OFF"
    boton_pantalla = Boton(centro_x - 180, 320, 360, 60, texto_pantalla, CREMA, AZUL, fuente)

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
                        boton_pantalla.texto = "Pantalla Completa: ON"
                    else:
                        ANCHO, ALTO = ANCHO_BASE, ALTO_BASE
                        ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                        boton_pantalla.texto = "Pantalla Completa: OFF"

                    actualizar_resolucion(ANCHO, ALTO)
                    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

                elif boton_volver.es_click(evento.pos):
                    # 🔧 Al volver, conserva el modo actual
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

        # 🟦 Escalar fuente principal y de botones
        tamaño_fuente_general = int(38 * escala_y)
        tamaño_fuente_botones = int(30 * escala_y)
        fuente_general = pygame.font.SysFont("Arial", tamaño_fuente_general, bold=True)
        fuente_botones = pygame.font.SysFont("Arial", tamaño_fuente_botones, bold=True)

        # 🟩 Dibujar botones actualizados
        for b in botones_ajustes:
            b.actualizar_posicion(escala_x, escala_y)
            # Ajustar fuente de cada botón al tamaño actual
            b.fuente = fuente_botones
            b.dibujar2(ventana)

        # 🟨 Texto del volumen centrado y escalado
        texto_volumen = fuente_general.render(f"Volumen: {int(volumen * 100)}%", True, BLANCO)
        pos_x = ANCHO // 2 - texto_volumen.get_width() // 2
        pos_y = int(180 * escala_y)
        ventana.blit(texto_volumen, (pos_x, pos_y))

        pygame.display.update()
