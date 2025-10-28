import pygame

# ===============================
# CLASE BOTÓN
# ===============================

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_fondo, color_texto, fuente,
                 color_hover=None, color_seleccion=None):
        self.x_base = x
        self.y_base = y
        self.ancho_base = ancho
        self.alto_base = alto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.fuente = fuente
        self.color_hover = color_hover if color_hover else color_fondo
        self.color_seleccion = color_seleccion if color_seleccion else (200, 220, 255)

    def actualizar_posicion(self, escala_x, escala_y):
        self.rect = pygame.Rect(
            int(self.x_base * escala_x),
            int(self.y_base * escala_y),
            int(self.ancho_base * escala_x),
            int(self.alto_base * escala_y)
        )

    def dibujar(self, ventana, mouse_pos, seleccionado=False, usar_hover=True):
        if seleccionado:
            color = self.color_seleccion
        elif usar_hover and mouse_pos and self.rect.collidepoint(mouse_pos):
            color = self.color_hover
        else:
            color = self.color_fondo

        pygame.draw.rect(ventana, color, self.rect, border_radius=20)
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        ventana.blit(
            texto_render,
            (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,
             self.rect.y + (self.rect.height - texto_render.get_height()) // 2)
        )

    def dibujar2(self, ventana):
        self.dibujar(ventana, mouse_pos=None, seleccionado=False, usar_hover=False)

    def es_click(self, pos):
        return self.rect.collidepoint(pos)
