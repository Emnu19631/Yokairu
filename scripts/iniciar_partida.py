import pygame
from config import CREMA, AZUL


# ===============================
# FUNCIÓN INICIAR PARTIDA
# ===============================
def iniciar_partida(ventana, ancho, alto, fuente):
    """Escena temporal de iniciar partida"""
    ventana.fill((30, 60, 120))
    texto = "Se está trabajando en esta función..."
    texto_render = fuente.render(texto, True, (255, 240, 200))
    ventana.blit(
        texto_render,
        ((ancho - texto_render.get_width()) // 2,
         (alto - texto_render.get_height()) // 2)
    )
    pygame.display.update()
    pygame.time.wait(2000)
