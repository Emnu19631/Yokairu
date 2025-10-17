import pygame
from config import cargar_imagen, cargar_audio, ANCHO_BASE, ALTO_BASE, ANCHO, ALTO, actualizar_resolucion, BLANCO, AZUL_OSCURO, CREMA, AZUL
from boton import Boton 

# ===============================
# DEFINICIÓN DE LA HISTORIA (PRIMERAS 4 SLIDES)
# ===============================
HISTORIA = [
    # SLIDE 1: Presentación (Narración)
    {
        "tipo": "narracion", 
        "fondo": "slide1.png", 
        "personaje": None,     
        "nombre": None,        
        "texto": None,         
        "next_slide": 1
    },
    # SLIDE 2: Elección de Género
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
    # SLIDE 3: Narración de Despertar
    {
        "tipo": "narracion", 
        "fondo": "slide3.png", 
        "personaje": None, 
        "nombre": None,        
        "texto": None,         
        "next_slide": 3
    },
    # SLIDE 4: Elección de Camino
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

# ===============================
# MOTOR DE LA NOVELA VISUAL
# ===============================
def ejecutar_novela(ventana, fuente):
    """Bucle principal para la novela visual."""
    
    global slide_index # Hacemos global el índice para que la función auxiliar lo vea
    slide_index = 0
    nv_activa = True
    botones_eleccion = []
    
    # --- Carga de Personajes (Mantenido) ---
    personajes_cache = {}
    def cargar_personaje(nombre_archivo):
        if not nombre_archivo: return None
        return None 

    # --- Creación de Botones de Elección (Función Auxiliar) ---
    def crear_botones_eleccion(slide, current_slide_index):
        from config import ANCHO, ALTO 
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        
        btns = []
        
        # =================================================================
        # === VALORES DE AJUSTE MANUAL (Slide 4) ===
        # =================================================================
        if slide["fondo"] == "slide4.png":
            # Si es el slide 4 (Elección de Camino)
            
            # --- POSICIÓN Y DIMENSIONES ---
            # Ajusta este valor para subir (disminuir) o bajar (aumentar) el bloque completo.
            inicio_y_base = ALTO_BASE * 0.60  
            # Punto de inicio X: El centro (ANCHO_BASE // 2) con un ajuste fino (ej: -100).
            x_inicio = ANCHO_BASE // 2 - 150 
            
            # Dimensiones de los botones
            btn_ancho = 300  
            btn_alto = 67
            
            # Espaciado
            espaciado_vertical = 70
            
        else:
            # Si es cualquier otro slide de elección (ej: Slide 2, Elección de Género)
            
            # --- POSICIÓN Y DIMENSIONES PREDETERMINADAS ---
            inicio_y_base = ALTO_BASE * 0.77 
            x_inicio = ANCHO_BASE // 2 - 100 
            btn_ancho = 250
            btn_alto = 60
            espaciado_vertical = 70
        # =================================================================
        
        for i, opcion in enumerate(slide["opciones"]):
            columna = i % 2
            fila = i // 2
            
            # Lógica para posicionar los botones en dos columnas
            x_base = x_inicio - 150 + columna * 300
            y_base = inicio_y_base + fila * espaciado_vertical 
            
            # Crea y ajusta el botón
            btn = Boton(x_base, y_base, btn_ancho, btn_alto, opcion["texto"], CREMA, AZUL, fuente, color_hover=AZUL_OSCURO)
            btn.actualizar_posicion(escala_x, escala_y)
            btns.append(btn)
            
        return btns

    # --- Bucle Principal de la Novela ---
    while nv_activa:
        from config import ANCHO, ALTO 
        mouse_pos = pygame.mouse.get_pos()
        escala_x = ANCHO / ANCHO_BASE
        escala_y = ALTO / ALTO_BASE
        
        if slide_index >= len(HISTORIA):
            return "menu" 

        slide = HISTORIA[slide_index]
        
        # Crear botones si es una slide de elección
        if slide["tipo"] == "eleccion" and not botones_eleccion:
            # === PASAMOS EL ÍNDICE ACTUAL PARA DIFERENCIAR ===
            botones_eleccion = crear_botones_eleccion(slide, slide_index) 


        # 1. Cargar y dibujar fondo
        fondo_actual = cargar_imagen(slide["fondo"], ANCHO, ALTO)
        ventana.blit(fondo_actual, (0, 0))


        # 2. Dibujar Botones de Elección (si aplica)
        if slide["tipo"] == "eleccion":
            for i, boton in enumerate(botones_eleccion):
                boton.actualizar_posicion(escala_x, escala_y)
                boton.dibujar(ventana, mouse_pos) 
                
        # 3. Manejo de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            
            # Manejar redimensionamiento
            elif evento.type == pygame.VIDEORESIZE:
                nuevo_ancho, nuevo_alto = evento.size
                actualizar_resolucion(nuevo_ancho, nuevo_alto) 
                if botones_eleccion:
                    # Se recrean los botones con el nuevo índice y proporciones
                    botones_eleccion = crear_botones_eleccion(slide, slide_index) 
                    
            
            # Evento de Avance (Click o Enter/Espacio)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                
                if slide["tipo"] == "narracion":
                    slide_index += 1
                    
                elif slide["tipo"] == "eleccion":
                    for i, boton in enumerate(botones_eleccion):
                        if boton.es_click(evento.pos):
                            print(f"Elegida opción: {boton.texto}")
                            botones_eleccion = []
                            # Usa el valor de 'next_slide' de la opción para saltar al siguiente índice
                            # En tu caso, todos apuntan al índice 4 (el siguiente al actual)
                            # Dejaremos un simple avance de 1 por ahora, hasta que definamos los saltos
                            slide_index += 1 
                            break 
                            
            # Avance con teclado (solo en diapositivas de narración)
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                 if slide["tipo"] == "narracion":
                    slide_index += 1

        pygame.display.update()
    
    return "menu"