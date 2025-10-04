import pygame

CREMA = (255, 240, 200)
AZUL = (100, 150, 255)

def mostrar_mensaje_en_desarrollo(ventana, ancho, alto, fuente):
    """Dibuja el mensaje de 'En desarrollo' en la ventana principal"""
    texto = "🚧 Esta función está en desarrollo 🚧"
    texto_render = fuente.render(texto, True, CREMA)
    # Fondo azul para resaltar
    fondo_rect = pygame.Rect(0, alto//2 - 60, ancho, 120)
    pygame.draw.rect(ventana, AZUL, fondo_rect)
    # Texto centrado
    ventana.blit(
        texto_render,
        ((ancho - texto_render.get_width()) // 2, alto//2 - texto_render.get_height() // 2)
    )
