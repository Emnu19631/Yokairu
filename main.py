import pygame
import sys
from src.guardado import guardar_partida, cargar_partida
from src.menu import mostrar_menu

pygame.init()
pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Mi primer juego con Pygame")

NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pantalla.fill(AZUL)
    pygame.display.flip()

if __name__ == "__main__":
    progreso = {"nivel": 1, "puntos": 50}
    guardar_partida(progreso)
    mostrar_menu()

pygame.quit()
sys.exit()

