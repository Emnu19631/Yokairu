import pygame
from config import cargar_imagen, cargar_audio, ANCHO_BASE, ALTO_BASE, ANCHO, ALTO, actualizar_resolucion, BLANCO, AZUL_OSCURO, CREMA, AZUL
from boton import Boton 

HISTORIA = [
    # Definición de los slides, cada uno tiene tipo (narración o elección), fondo, personaje y texto.
    # Slide 1: Narración
    {
        "tipo": "narracion", 
        "fondo": "slide1.png", 
        "personaje": None,     
        "nombre": None,        
        "texto": None,         
        "next_slide": 1
    },
    # Slide 2: Elección de Género
    {
        "tipo": "eleccion",
        "fondo": "slide2.png", 
        "personaje": None,
        "nombre": None,        
        "texto": None,         
        "opciones": [
            {"texto": "Hombre", "next_slide": 2}, 
            {"texto": "Mujer", "next_slide": 2}, 
        ],
    },
    # Slide 3: Narración de Despertar
    {
        "tipo": "narracion", 
        "fondo": "slide3.png", 
        "personaje": None, 
        "nombre": None,        
        "texto": None,         
        "next_slide": 3
    },
    # Slide 4: Elección de Camino
    {
        "tipo": "eleccion",
        "fondo": "slide4.png", 
        "personaje": None,
        "nombre": None,        
        "texto": None,         
        "opciones": [
            {"texto": "Al pueblo", "next_slide": 4},
            {"texto": "A la isla", "next_slide": 4},
            {"texto": "Al prado", "next_slide": 4},
            {"texto": "Al volcán", "next_slide": 4},
        ],
    },
]

def ejecutar_novela(ventana, fuente):
    """Bucle principal que gestiona el avance de la novela visual."""
    
    global slide_index 
    slide_index = 0
    nv_activa = True
    botones_eleccion = []
    
    # Función para cargar personajes (sin implementación aquí)
    def cargar_personaje(nombre_archivo):
        if not nombre_archivo: return None
        return None 

    # Función que crea los botones de elección según el slide actual
    def crear_botones_eleccion(slide, current_slide_index):
        from config import ANCHO, ALTO 
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        
        btns = []
        
        # Si es el Slide 4, ajustamos manualmente la posición de los botones
        if slide["fondo"] == "slide4.png":
            inicio_y_base = ALTO_BASE * 0.60  
            x_inicio = ANCHO_BASE // 2 - 150 
            btn_ancho = 300  
            btn_alto = 67
            espaciado_vertical = 70
        else:
            # Para el resto de slides de elección, se usan posiciones predeterminadas
            inicio_y_base = ALTO_BASE * 0.77 
            x_inicio = ANCHO_BASE // 2 - 100 
            btn_ancho = 250
            btn_alto = 60
            espaciado_vertical = 70
        
        # Crear botones basados en las opciones del slide
        for i, opcion in enumerate(slide["opciones"]):
            columna = i % 2
            fila = i // 2
            x_base = x_inicio - 150 + columna * 300
            y_base = inicio_y_base + fila * espaciado_vertical 
            btn = Boton(x_base, y_base, btn_ancho, btn_alto, opcion["texto"], CREMA, AZUL, fuente, color_hover=AZUL_OSCURO)
            btn.actualizar_posicion(escala_x, escala_y)
            btns.append(btn)
        
        return btns

    # Bucle principal donde se actualiza el estado de la novela visual
    while nv_activa:
        mouse_pos = pygame.mouse.get_pos()
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        
        if slide_index >= len(HISTORIA):
            return "menu" 

        slide = HISTORIA[slide_index]
        
        # Crear botones si es una slide de elección
        if slide["tipo"] == "eleccion" and not botones_eleccion:
            botones_eleccion = crear_botones_eleccion(slide, slide_index) 

        # 1. Cargar y dibujar fondo
        fondo_actual = cargar_imagen(slide["fondo"], ANCHO, ALTO)
        ventana.blit(fondo_actual, (0, 0))

        # 2. Dibujar botones de elección
        if slide["tipo"] == "eleccion":
            for boton in botones_eleccion:
                boton.actualizar_posicion(escala_x, escala_y)
                boton.dibujar(ventana, mouse_pos) 
                
        # 3. Manejo de eventos de usuario (clicks, redimensionamiento, teclado)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            
            elif evento.type == pygame.VIDEORESIZE:
                nuevo_ancho, nuevo_alto = evento.size
                actualizar_resolucion(nuevo_ancho, nuevo_alto)
                if botones_eleccion:
                    botones_eleccion = crear_botones_eleccion(slide, slide_index)
            
            # Avance mediante click
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if slide["tipo"] == "narracion":
                    slide_index += 1
                elif slide["tipo"] == "eleccion":
                    for boton in botones_eleccion:
                        if boton.es_click(evento.pos):
                            print(f"Elegida opción: {boton.texto}")
                            botones_eleccion = []  # Limpiar botones
                            slide_index += 1 
                            break 
                            
            # Avance con teclado (solo en narración)
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                 if slide["tipo"] == "narracion":
                    slide_index += 1

        pygame.display.update()
    
    return "menu"
