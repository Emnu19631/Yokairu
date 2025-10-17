import pygame
from boton import Boton
from config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION,
    ALTO_BASE, CREMA, AZUL, BLANCO, actualizar_resolucion, cargar_imagen
)

# Función que maneja la pantalla de ajustes del juego.
# Aquí se gestionan opciones como el volumen y el modo de pantalla completa.
def pantalla_ajustes(fuente):
    global ventana, fondo, ANCHO, ALTO
    ajustes_activo = True  # Bandera para controlar el bucle de ajustes
    volumen = pygame.mixer.music.get_volume()  # Obtiene el volumen actual de la música

    # Determina si la ventana está en pantalla completa
    fullscreen_actual = ventana.get_flags() & pygame.FULLSCREEN
    pantalla_completa = bool(fullscreen_actual)

    # Calcula la posición X centrada para los botones
    centro_x = ANCHO_BASE // 2  

    # Crea botones para ajustar el volumen y la pantalla
    boton_volumen_mas = Boton(centro_x + 150, 170, 60, 50, "+", CREMA, AZUL, fuente)
    boton_volumen_menos = Boton(centro_x - 200, 170, 60, 50, "-", CREMA, AZUL, fuente)

    # Texto que muestra el estado de la pantalla completa (ON/OFF)
    texto_pantalla = "Pantalla Completa: ON" if pantalla_completa else "Pantalla Completa: OFF"
    boton_pantalla = Boton(centro_x - 180, 320, 360, 60, texto_pantalla, CREMA, AZUL, fuente)

    boton_volver = Boton(centro_x - 110, 390, 220, 50, "Volver", CREMA, AZUL, fuente)

    # Lista de botones en la pantalla de ajustes
    botones_ajustes = [boton_volumen_mas, boton_volumen_menos, boton_pantalla, boton_volver]

    # Carga el fondo de la pantalla
    fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)

    # Bucle principal de la pantalla de ajustes
    while ajustes_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si se cierra la ventana
                ajustes_activo = False
                return "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Ajusta el volumen al presionar el botón "+"
                if boton_volumen_mas.es_click(evento.pos):
                    volumen = min(1.0, volumen + 0.1)
                    pygame.mixer.music.set_volume(volumen)

                # Ajusta el volumen al presionar el botón "-"
                elif boton_volumen_menos.es_click(evento.pos):
                    volumen = max(0.0, volumen - 0.1)
                    pygame.mixer.music.set_volume(volumen)

                # Cambia entre pantalla completa y ventana normal
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

                # Vuelve a la pantalla anterior
                elif boton_volver.es_click(evento.pos):
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
        # DIBUJAR ELEMENTOS EN PANTALLA
        # ===============================
        escala_x = ANCHO / ANCHO_BASE  # Factor de escala horizontal
        escala_y = ALTO / ALTO_BASE  # Factor de escala vertical

        # Dibuja el fondo de la pantalla
        ventana.blit(fondo, (0, 0))

        # Calcula el tamaño de las fuentes escaladas según la resolución actual
        tamaño_fuente_general = int(38 * escala_y)
        tamaño_fuente_botones = int(30 * escala_y)
        fuente_general = pygame.font.SysFont("Arial", tamaño_fuente_general, bold=True)
        fuente_botones = pygame.font.SysFont("Arial", tamaño_fuente_botones, bold=True)

        # Actualiza y dibuja los botones en su nueva posición y tamaño escalado
        for b in botones_ajustes:
            b.actualizar_posicion(escala_x, escala_y)
            b.fuente = fuente_botones  # Asigna la fuente escalada
            b.dibujar2(ventana)  # Dibuja el botón

        # Dibuja el texto del volumen en la pantalla
        texto_volumen = fuente_general.render(f"Volumen: {int(volumen * 100)}%", True, BLANCO)
        pos_x = ANCHO // 2 - texto_volumen.get_width() // 2  # Centra el texto
        pos_y = int(180 * escala_y)  # Posición Y escalada
        ventana.blit(texto_volumen, (pos_x, pos_y))  # Dibuja el texto en la pantalla

        # Actualiza la pantalla
        pygame.display.update()
