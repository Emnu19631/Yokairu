import pygame
from ui.boton import Boton
from core.config import ANCHO, ALTO, cargar_imagen, CREMA, AZUL, BLANCO, AZUL_RESALTADO, PANTALLA_COMPLETA
from core.render import mostrar_texto_tipeado_con_fondo_solido
from game.historia import HISTORIA

# ===============================
# BOTONES DE NAVEGACIÓN
# ===============================

def crear_botones_navegacion(ancho, fuente):
    boton_inicio = Boton(ancho - 260, 10, 120, 50, "Inicio", CREMA, AZUL, fuente, color_hover=AZUL_RESALTADO)
    boton_ajustes = Boton(ancho - 120, 10, 120, 50, "Ajustes", CREMA, AZUL, fuente, color_hover=AZUL_RESALTADO)
    return boton_inicio, boton_ajustes

def dibujar_botones_navegacion(ventana, mouse_pos, boton_inicio, boton_ajustes):
    boton_inicio.dibujar(ventana, mouse_pos)
    boton_ajustes.dibujar(ventana, mouse_pos)

# ===============================
# IMÁGENES Y TEXTO
# ===============================

def cargar_y_dibujar_imagen(slide, ventana, ancho, alto):
    if "imagen" not in slide:
        return None, None
    img = cargar_imagen(slide["imagen"])
    ancho_original, alto_original = img.get_size()
    escala_x = ancho / 800
    escala_y = alto / 450
    scalar = slide.get("scalar", 1)
    img = pygame.transform.scale(img, (int(ancho_original * scalar * escala_x), int(alto_original * scalar * escala_y)))
    pos_rel = slide.get("pos_rel", (0.1, 0.1))
    is_fullscreen = ventana.get_flags() & pygame.FULLSCREEN
    desplazamiento_y = 0.2 * alto if is_fullscreen else 0
    pos = (int(pos_rel[0] * ancho), int(pos_rel[1] * alto + desplazamiento_y))
    ventana.blit(img, pos)
    return img, pos

def manejar_texto_y_botones(slide, ventana, fuente, fondo, boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index):
    texto = slide.get("texto", "")
    if not texto:
        return None
    rect_texto = pygame.Rect(50, alto - 160, ancho - 100, 150)
    salir = mostrar_texto_con_botones_visibles(
        ventana, fuente, texto, (0, 0, 0), rect_texto, fondo,
        boton_inicio, boton_ajustes, img, pos
    )
    if salir == "inicio":
        return "inicio"
    elif salir == "ajustes":
        return f"ajustes:{slide_index}"
    elif salir is True:
        return "salir"
    return None

# ===============================
# ELECCIONES Y EVENTOS
# ===============================

def ajustar_tamano_boton_y_fuente(texto, ancho_base=200, alto_base=50, fuente_base=24):
    largo = len(texto)
    if largo > 20:
        escala = min(1.0, 20 / largo)
        ancho = int(ancho_base * (1 + (1 - escala) * 0.6))
        alto = int(alto_base * (1 + (1 - escala) * 0.5))
        fuente_tam = int(fuente_base * escala * 0.9)
    else:
        ancho, alto, fuente_tam = ancho_base, alto_base, fuente_base
    return ancho, alto, fuente_tam



def manejar_opciones(slide, fuente, ancho, alto):
    opciones = slide["opciones"]
    layout = slide.get("layout", "horizontal")
    botones_opciones = []
    rect_opciones = pygame.Rect(50, alto - 160, ancho - 100, 150)
    color_fondo = (234, 210, 146)

    if layout == "horizontal":
        espacio_total = len(opciones) * 200 + (len(opciones) - 1) * 40
        inicio_x = ancho // 2 - espacio_total // 2
        y = alto - 100
        for i, opcion in enumerate(opciones):
            boton_ancho, boton_alto, fuente_tam = ajustar_tamano_boton_y_fuente(opcion["texto"])
            fuente_boton = pygame.font.SysFont("Arial", fuente_tam, bold=True)
            boton = Boton(inicio_x + i * 240, y, boton_ancho, boton_alto, opcion["texto"], CREMA, AZUL, fuente_boton, color_hover=AZUL_RESALTADO)
            botones_opciones.append((boton, opcion["next"]))
    else:
        boton_ancho, boton_alto, espacio = 180, 45, 20
        total_ancho = boton_ancho * 2 + espacio
        total_alto = boton_alto * 2 + espacio
        inicio_x = rect_opciones.centerx - total_ancho // 2
        inicio_y = rect_opciones.centery - total_alto // 2
        posiciones = [
            (inicio_x, inicio_y),
            (inicio_x + boton_ancho + espacio, inicio_y),
            (inicio_x, inicio_y + boton_alto + espacio),
            (inicio_x + boton_ancho + espacio, inicio_y + boton_alto + espacio)
        ]
        for opcion, pos in zip(opciones, posiciones):
            boton_ancho, boton_alto, fuente_tam = ajustar_tamano_boton_y_fuente(opcion["texto"], 180, 45, 24)
            fuente_boton = pygame.font.SysFont("Arial", fuente_tam, bold=True)
            boton = Boton(pos[0], pos[1], boton_ancho, boton_alto, opcion["texto"], CREMA, AZUL, fuente_boton, color_hover=AZUL_RESALTADO)
            botones_opciones.append((boton, opcion["next"]))

    return botones_opciones, rect_opciones, color_fondo


def esperar_eleccion(ventana, fondo, img, pos, botones_opciones, rect_opciones, color_fondo, boton_inicio, boton_ajustes, slide_index):
    while True:
        _dibujar_pantalla(ventana, fondo, img, pos, rect_opciones, color_fondo, botones_opciones, boton_inicio, boton_ajustes)
        accion = _manejar_eventos(boton_inicio, boton_ajustes, botones_opciones, slide_index)
        if accion:
            return accion

def _dibujar_pantalla(ventana, fondo, img, pos, rect_opciones, color_fondo, botones_opciones, boton_inicio, boton_ajustes):
    mouse_pos = pygame.mouse.get_pos()
    ventana.blit(fondo, (0, 0))
    if img:
        ventana.blit(img, pos)
    pygame.draw.rect(ventana, color_fondo, rect_opciones, border_radius=10)
    dibujar_botones_navegacion(ventana, mouse_pos, boton_inicio, boton_ajustes)
    for boton, _ in botones_opciones:
        boton.dibujar(ventana, mouse_pos)
    pygame.display.update()

def _manejar_eventos(boton_inicio, boton_ajustes, botones_opciones, slide_index):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return "salir"
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            return _procesar_click(e.pos, boton_inicio, boton_ajustes, botones_opciones, slide_index)
    return None

def _procesar_click(pos, boton_inicio, boton_ajustes, botones_opciones, slide_index):
    if boton_inicio.es_click(pos):
        return "inicio"
    if boton_ajustes.es_click(pos):
        return f"ajustes:{slide_index}"
    for boton, destino in botones_opciones:
        if boton.es_click(pos):
            return destino
    return None

# ===============================
# EJECUCIÓN PRINCIPAL
# ===============================

def ejecutar_novela(ventana, fuente, ancho, alto, slide_inicial=0):
    slide_index = slide_inicial
    boton_inicio, boton_ajustes = crear_botones_navegacion(ancho, fuente)
    while slide_index < len(HISTORIA):
        slide = HISTORIA[slide_index]
        fondo_actual = preparar_fondo(slide, ventana, ancho, alto)
        if slide["tipo"] == "narracion":
            accion, slide_index = procesar_narracion(slide, ventana, fuente, fondo_actual,
                                                     boton_inicio, boton_ajustes, ancho, alto, slide_index)
        elif slide["tipo"] == "eleccion":
            accion, slide_index = procesar_eleccion(slide, ventana, fuente, fondo_actual,
                                                    boton_inicio, boton_ajustes, ancho, alto, slide_index)
        else:
            accion = None
        if accion in ["inicio", "salir"] or (isinstance(accion, str) and accion.startswith("ajustes")):
            return accion
    return "menu"

# ===============================
# PROCESAMIENTO DE SLIDES
# ===============================

def preparar_fondo(slide, ventana, ancho, alto):
    if "transicion_fondos" in slide:
        for img in slide["transicion_fondos"]:
            fondo_trans = cargar_imagen(img, ancho, alto)
            ventana.blit(fondo_trans, (0, 0))
            pygame.display.update()
            pygame.time.delay(150)
        fondo_actual = cargar_imagen(slide["transicion_fondos"][-1], ancho, alto)
    else:
        fondo_actual = cargar_imagen(slide["fondo"], ancho, alto)
    ventana.blit(fondo_actual, (0, 0))
    return fondo_actual

def procesar_narracion(slide, ventana, fuente, fondo_actual, boton_inicio, boton_ajustes, ancho, alto, slide_index):
    img, pos = cargar_y_dibujar_imagen(slide, ventana, ancho, alto)
    dibujar_botones_navegacion(ventana, pygame.mouse.get_pos(), boton_inicio, boton_ajustes)
    pygame.display.update()
    accion = manejar_texto_y_botones(slide, ventana, fuente, fondo_actual,
                                     boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index)
    if accion:
        return accion, slide_index
    if "next" in slide:
        return None, slide["next"]
    return None, slide_index + 1


def procesar_eleccion(slide, ventana, fuente, fondo_actual, boton_inicio, boton_ajustes, ancho, alto, slide_index):
    img, pos = cargar_y_dibujar_imagen(slide, ventana, ancho, alto)
    dibujar_botones_navegacion(ventana, pygame.mouse.get_pos(), boton_inicio, boton_ajustes)
    pygame.display.update()
    accion = manejar_texto_y_botones(slide, ventana, fuente, fondo_actual,
                                     boton_inicio, boton_ajustes, ancho, alto, img, pos, slide_index)
    if accion:
        return accion, slide_index
    botones_opciones, rect_opciones, color_fondo = manejar_opciones(slide, fuente, ancho, alto)
    accion = esperar_eleccion(ventana, fondo_actual, img, pos,
                              botones_opciones, rect_opciones, color_fondo,
                              boton_inicio, boton_ajustes, slide_index)
    return accion, accion

# ===============================
# TEXTO CON BOTONES VISIBLES
# ===============================

def mostrar_texto_con_botones_visibles(ventana, fuente_inicial, texto, color, rect, fondo,
                                       boton_inicio, boton_ajustes, imagen=None, pos_imagen=None):
    reloj = pygame.time.Clock()
    indice, texto_mostrado, texto_completo = 0, "", False
    tiempo_ultimo = pygame.time.get_ticks()
    while not texto_completo:
        accion = _manejar_eventos_texto(boton_inicio, boton_ajustes)
        if accion == "completar":
            texto_mostrado = texto
            texto_completo = True
        elif accion in ("inicio", "ajustes", True):
            return accion
        texto_mostrado, indice, texto_completo, tiempo_ultimo = _actualizar_texto(
            texto, texto_mostrado, indice, texto_completo, tiempo_ultimo
        )
        _dibujar_pantalla_texto(
            ventana, fondo, imagen, pos_imagen, boton_inicio, boton_ajustes,
            fuente_inicial, texto_mostrado, color, rect
        )
        reloj.tick(60)
    return _esperar_confirmacion_final(boton_inicio, boton_ajustes)

# ===============================
# EVENTOS DE TEXTO
# ===============================

def _manejar_eventos_texto(boton_inicio, boton_ajustes):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return True
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_inicio.es_click(evento.pos):
                return "inicio"
            if boton_ajustes.es_click(evento.pos):
                return "ajustes"
            return "completar"
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            return "completar"
    return None

def _actualizar_texto(texto, mostrado, indice, completo, tiempo_ultimo):
    tiempo_actual = pygame.time.get_ticks()
    if not completo and tiempo_actual - tiempo_ultimo > 50:
        if indice < len(texto):
            mostrado += texto[indice]
            indice += 1
            tiempo_ultimo = tiempo_actual
        else:
            completo = True
    return mostrado, indice, completo, tiempo_ultimo

def _dibujar_pantalla_texto(ventana, fondo, imagen, pos_imagen, boton_inicio, boton_ajustes,
                            fuente_inicial, texto_mostrado, color, rect):
    from core.render import ajustar_fuente_al_rect
    ventana.blit(fondo, (0, 0))
    if imagen and pos_imagen:
        ventana.blit(imagen, pos_imagen)
    mouse_pos = pygame.mouse.get_pos()
    boton_inicio.dibujar(ventana, mouse_pos)
    boton_ajustes.dibujar(ventana, mouse_pos)
    ventana.fill((234, 210, 146), rect)
    fuente_ajustada, lineas = ajustar_fuente_al_rect(texto_mostrado, fuente_inicial, rect)
    y = rect.y + 10
    for linea in lineas:
        render = fuente_ajustada.render(linea, True, color)
        ventana.blit(render, (rect.x + 10, y))
        y += fuente_ajustada.get_height() + 2
    pygame.display.update()

def _esperar_confirmacion_final(boton_inicio, boton_ajustes):
    while True:
        for evento in pygame.event.get():
            accion = _procesar_evento_final(evento, boton_inicio, boton_ajustes)
            if accion is not None:
                return accion

def _procesar_evento_final(evento, boton_inicio, boton_ajustes):
    if evento.type == pygame.QUIT:
        return True
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if boton_inicio.es_click(evento.pos):
            return "inicio"
        if boton_ajustes.es_click(evento.pos):
            return "ajustes"
        return False
    if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
        return False
    return None
