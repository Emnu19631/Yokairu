import pygame
import sys
from src.guardado import guardar_partida, cargar_partida
from src.juego import iniciar_juego

def mostrar_menu():
    pygame.init()
    pantalla = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Menú del Juego")

    fuente = pygame.font.SysFont("Arial", 28)
    botones = {
        "jugar": pygame.Rect(200, 100, 200, 50),
        "cargar": pygame.Rect(200, 170, 200, 50),
        "salir": pygame.Rect(200, 240, 200, 50)
    }

    progreso = {"nivel": 1, "puntos": 0}
    running = True

    while running:
        pantalla.fill((30, 30, 50))
        for nombre, rect in botones.items():
            pygame.draw.rect(pantalla, (100, 150, 200), rect)
            texto = fuente.render(nombre.capitalize(), True, (255, 255, 255))
            pantalla.blit(texto, (rect.x + 60, rect.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                guardar_partida(progreso)
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if botones["jugar"].collidepoint(pos):
                    iniciar_juego()  # Llama al juego real

                elif botones["cargar"].collidepoint(pos):
                    data = cargar_partida()
                    if data:
                        progreso = data

                elif botones["salir"].collidepoint(pos):
                    guardar_partida(progreso)
                    pygame.quit()
                    sys.exit()
    pygame.quit()

