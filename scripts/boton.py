import pygame


# ===============================
# CLASE BOTÓN
# ===============================
class Boton:
    # Inicializa las propiedades del botón (posición, tamaño, texto, colores, fuente)
    def __init__(self, x, y, ancho, alto, texto, color_fondo, color_texto, fuente,
                 color_hover=None, color_seleccion=None):
        self.x_base = x  # Posición X inicial del botón
        self.y_base = y  # Posición Y inicial del botón
        self.ancho_base = ancho  # Ancho base del botón
        self.alto_base = alto  # Alto base del botón
        self.rect = pygame.Rect(x, y, ancho, alto)  # Área rectangular del botón
        self.texto = texto  # Texto que se muestra en el botón
        self.color_fondo = color_fondo  # Color de fondo del botón
        self.color_texto = color_texto  # Color del texto
        self.fuente = fuente  # Fuente del texto
        self.color_hover = color_hover if color_hover else color_fondo  # Color al pasar el ratón
        self.color_seleccion = color_seleccion if color_seleccion else (200, 220, 255)  # Color al seleccionar

    # Actualiza la posición y el tamaño del botón según la resolución de la ventana
    def actualizar_posicion(self, escala_x, escala_y):
        self.rect = pygame.Rect(
            int(self.x_base * escala_x),  # Ajuste de la posición X
            int(self.y_base * escala_y),  # Ajuste de la posición Y
            int(self.ancho_base * escala_x),  # Ajuste del ancho
            int(self.alto_base * escala_y)   # Ajuste del alto
        )

    # Dibuja el botón en la ventana con efectos de hover o seleccionado
    def dibujar(self, ventana, mouse_pos, seleccionado=False, usar_hover=True):
        if seleccionado:
            color = self.color_seleccion  # Color cuando el botón está seleccionado
        elif usar_hover and self.rect.collidepoint(mouse_pos):
            color = self.color_hover  # Color cuando el mouse está sobre el botón
        else:
            color = self.color_fondo  # Color normal del botón

        pygame.draw.rect(ventana, color, self.rect, border_radius=20)  # Dibuja el fondo del botón
        texto_render = self.fuente.render(self.texto, True, self.color_texto)  # Renderiza el texto
        ventana.blit(
            texto_render,
            (self.rect.x + (self.rect.width - texto_render.get_width()) // 2,  # Centra el texto en X
             self.rect.y + (self.rect.height - texto_render.get_height()) // 2)  # Centra el texto en Y
        )

    # Dibuja el botón sin hover ni selección
    def dibujar2(self, ventana):
        self.dibujar(ventana, mouse_pos=None, seleccionado=False, usar_hover=False)

    # Verifica si un clic está dentro del área del botón
    def es_click(self, pos):
        return self.rect.collidepoint(pos)
