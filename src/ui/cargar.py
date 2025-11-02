import pygame
from core.config import ventana, ANCHO, ALTO, actualizar_resolucion, cargar_imagen, CREMA, AZUL, background_juego, PANTALLA_COMPLETA, PROPORCION
from ui.boton import Boton
from game.save_system import listar_guardados, cargar_partida_por_id
from game.historia import HISTORIA

SLOTS_VISIBLES = 2
THUMB_SIZE = (140, 80)
PADDING = 12
scroll_offset = 0.0
scroll_target = 0.0
SCROLL_SPEED = 0.18


def _obtener_miniatura_para_slot(slot):
    slide_index = slot.get("slide", 0)
    try:
        slide = HISTORIA[slide_index]
    except Exception:
        return None

    nombre = slide.get("imagen") or slide.get("fondo")
    if nombre:
        try:
            img = cargar_imagen(nombre)
            return pygame.transform.scale(img, THUMB_SIZE)
        except Exception:
            return None
    return None


# ===============================
# Sub-funciones para eventos
# ===============================

def _evento_quit(e):
    if e.type == pygame.QUIT:
        return "quit"
    return None


def _evento_scroll(e, max_scroll):
    global scroll_target
    if e.type == pygame.MOUSEWHEEL:
        scroll_target -= e.y * 40
        scroll_target = max(0, min(scroll_target, max_scroll))
        return "ok"
    return None


def _slot_clicado(e, boton, slot):
    if boton.es_click(e.pos):
        data = cargar_partida_por_id(slot["id"])
        return data.get("slide") if data else None
    return "ok"


def _click_en_slots(e, botones_slots, limite_superior, limite_inferior):
    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        for boton, slot in botones_slots:
            if limite_superior <= boton.rect.y <= limite_inferior - boton.rect.height:
                r = _slot_clicado(e, boton, slot)
                if isinstance(r, int) or r is None:
                    return r
    return "ok"



def _click_volver(e, boton_volver):
    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        if boton_volver.es_click(e.pos):
            return None
    return "ok"


def _evento_resize(e):
    if e.type == pygame.VIDEORESIZE:
        global ANCHO, ALTO, ventana, background_juego
        ANCHO, ALTO = e.size
        ALTO = int(ANCHO / PROPORCION)
        actualizar_resolucion(ANCHO, ALTO)
        ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
        background_juego = cargar_imagen("background_juego.jpg", ANCHO, ALTO)


def _procesar_eventos(max_scroll, botones_slots, limite_superior, limite_inferior, boton_volver):
    for e in pygame.event.get():

        r = _evento_quit(e)
        if r == "quit":
            return r

        _evento_scroll(e, max_scroll)

        r = _click_en_slots(e, botones_slots, limite_superior, limite_inferior)
        if isinstance(r, int):
            return r

        r = _click_volver(e, boton_volver)
        if r is None:
            return None

        _evento_resize(e)

    return "continuar"


# ===============================
# Sub-función de dibujo
# ===============================
def _dibujar_titulo(fuente):
    titulo = fuente.render("CARGAR PARTIDA", True, AZUL)
    ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2,
                          int(ALTO * 0.1)))


def _dibujar_slots(saves, fuente, mouse_pos,
                   limite_superior, limite_inferior,
                   slot_h, espacio_total,
                   start_y, ancho_slot, x_slot):

    botones_slots = []

    clip_rect = pygame.Rect(0, limite_superior, ANCHO, limite_inferior - limite_superior)
    ventana.set_clip(clip_rect)

    for i, slot in enumerate(saves):
        y = start_y + (i * espacio_total) - scroll_offset

        if y + slot_h < limite_superior or y > limite_inferior:
            continue

        boton = Boton(x_slot, int(y), ancho_slot, slot_h, "", CREMA, AZUL, fuente)
        boton.actualizar_posicion(1, 1)
        botones_slots.append((boton, slot))
        boton.dibujar(ventana, mouse_pos)

        mini = _obtener_miniatura_para_slot(slot)
        if mini:
            ventana.blit(mini, (boton.rect.x + 8, boton.rect.y + 6))

        fecha = slot.get("fecha", "")
        try:
            fecha_bonita = f"{fecha[8:10]}/{fecha[5:7]}/{fecha[:4]} – {fecha[11:16]}"
        except Exception:
            fecha_bonita = fecha

        txt = fuente.render(fecha_bonita, True, AZUL)
        ventana.blit(txt, (
            boton.rect.x + THUMB_SIZE[0] + 24,
            boton.rect.y + boton.rect.height // 2 - txt.get_height() // 2
        ))

    ventana.set_clip(None)
    return botones_slots


# ===============================
# FUNCIÓN PRINCIPAL
# ===============================
def pantalla_cargar(fuente):
    global scroll_offset, scroll_target, ventana, ANCHO, ALTO, background_juego

    clock = pygame.time.Clock()

    while True:
        saves = listar_guardados()

        ANCHO, ALTO = ventana.get_size()
        actualizar_resolucion(ANCHO, ALTO)
        background_juego = cargar_imagen("background_juego.jpg", ANCHO, ALTO)

        ventana.blit(background_juego, (0, 0))
        _dibujar_titulo(fuente)
        mouse_pos = pygame.mouse.get_pos()

        limite_superior = int(ALTO * 0.22)
        limite_inferior = ALTO - 120
        zona_scroll_altura = limite_inferior - limite_superior

        slot_h = THUMB_SIZE[1] + 2 * PADDING
        espacio_total = slot_h + 18
        total_altura_slots = len(saves) * espacio_total
        max_scroll = max(0, total_altura_slots - zona_scroll_altura)

        scroll_offset += (scroll_target - scroll_offset) * 0.08

        start_y = limite_superior
        ancho_slot = ANCHO - 200
        x_slot = 100

        botones_slots = _dibujar_slots(
            saves, fuente, mouse_pos,
            limite_superior, limite_inferior,
            slot_h, espacio_total,
            start_y, ancho_slot, x_slot
        )

        if not saves:
            txt = fuente.render("No hay partidas guardadas", True, AZUL)
            ventana.blit(txt, (ANCHO // 2 - txt.get_width() // 2, ALTO // 2))

        boton_volver = Boton(ANCHO // 2 - 100, ALTO - 80, 200, 50,
                             "Volver", CREMA, AZUL, fuente)
        boton_volver.dibujar(ventana, mouse_pos)

        resultado = _procesar_eventos(max_scroll, botones_slots,
                                      limite_superior, limite_inferior,
                                      boton_volver)

        if resultado == "quit":
            return None
        if isinstance(resultado, int):
            # devolver el id del slot, no el número del slide
            return next((slot["id"] for boton, slot in botones_slots if slot.get("slide") == resultado), None)

        if resultado is None:
            return None


        pygame.display.update()
        clock.tick(60)
