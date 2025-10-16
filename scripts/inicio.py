import pygame
import sys
from guardar import guardar_partida, cargar_partida
from iniciar_partida import iniciar_partida 
from boton import Boton
from config import (
    ventana, fondo, ANCHO, ALTO, ANCHO_BASE, PROPORCION, ALTO_BASE, CREMA, AZUL, 
    BLANCO, AZUL_OSCURO, AZUL_RESALTADO, actualizar_resolucion, cargar_imagen, 
    cargar_audio, bloquear_maximizar
)
from ajustes import pantalla_ajustes
from config import cargar_imagen, cargar_audio, bloquear_maximizar


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
# MENÚ PRINCIPAL
# ===============================
boton_ancho = 180
boton_alto = 35
espaciado = 15
inicio_y = 200
botones_textos = ["Iniciar", "Cargar", "Ajustes", "Salir"]
botones = []

for i, texto in enumerate(botones_textos):
    x = ANCHO_BASE // 2 - boton_ancho // 2
    y = inicio_y + i * (boton_alto + espaciado)
    botones.append(Boton(x, y, boton_ancho, boton_alto, texto, CREMA, AZUL, fuente))


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
            # Asegura mantener la proporción
            ALTO = int(ANCHO / PROPORCION)
            actualizar_resolucion(ANCHO, ALTO)
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            fondo = cargar_imagen("background_inicio.jpg", ANCHO, ALTO)
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
                    # === CAMBIO CLAVE AQUÍ: MANEJO DEL RESULTADO DE iniciar_partida (Teclado) ===
                    resultado = iniciar_partida(ventana, ANCHO, ALTO, fuente)
                    if resultado == "salir":
                        corriendo = False
                elif texto == "Ajustes":
                    resultado = pantalla_ajustes(fuente)
                    if resultado == "salir":
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
                            # === CAMBIO CLAVE AQUÍ: MANEJO DEL RESULTADO DE iniciar_partida (Ratón) ===
                            resultado = iniciar_partida(ventana, ANCHO, ALTO, fuente)
                            if resultado == "salir":
                                corriendo = False
                        elif texto == "Ajustes":
                            resultado = pantalla_ajustes(fuente)
                            if resultado == "salir":
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