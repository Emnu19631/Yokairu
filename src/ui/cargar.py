import pygame
from core.config import ventana, ANCHO, ALTO, actualizar_resolucion, cargar_imagen, CREMA, AZUL, background_juego, PANTALLA_COMPLETA, PROPORCION
from ui.boton import Boton
from game.save_system import listar_guardados, cargar_partida_por_id
from game.historia import HISTORIA

# configuración visual
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
        except:
            return None
    return None


def pantalla_cargar(fuente):
    global scroll_offset, scroll_target, ventana, ANCHO, ALTO, background_juego

    activo = True
    clock = pygame.time.Clock()

    while activo:
        saves = listar_guardados()

        # Recalcular dimensiones
        ANCHO, ALTO = ventana.get_size()
        actualizar_resolucion(ANCHO, ALTO)
        background_juego = cargar_imagen("background_juego.jpg", ANCHO, ALTO)

        # ================================
        # EVENTOS
        # ================================
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None

            if e.type == pygame.MOUSEWHEEL:
                scroll_target -= e.y * 40
                scroll_target = max(0, min(scroll_target, max_scroll))

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Comprobar si se clicó dentro de la zona visible del scroll
                for boton, slot in botones_slots:
                    # Evitar clics en botones fuera del área visible
                    if limite_superior <= boton.rect.y <= limite_inferior - boton.rect.height:
                        if boton.es_click(e.pos):
                            data = cargar_partida_por_id(slot["id"])
                            return data.get("slide") if data else None

                # Clic en botón volver
                if boton_volver.es_click(e.pos):
                    return None


            if e.type == pygame.VIDEORESIZE:
                ANCHO, ALTO = e.size
                ALTO = int(ANCHO / PROPORCION)
                actualizar_resolucion(ANCHO, ALTO)
                ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                background_juego = cargar_imagen("background_juego.jpg", ANCHO, ALTO)

        # ================================
        # DIBUJO DE FONDO Y TÍTULO
        # ================================
        ventana.blit(background_juego, (0, 0))
        titulo = fuente.render("CARGAR PARTIDA", True, AZUL)
        titulo_y = int(ALTO * 0.1)
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, titulo_y))

        mouse_pos = pygame.mouse.get_pos()
        botones_slots = []

        # ================================
        # CONFIGURACIÓN DEL SCROLL
        # ================================
        limite_superior = int(ALTO * 0.22)   # debajo del título
        limite_inferior = ALTO - 120         # justo encima del botón
        zona_scroll_altura = limite_inferior - limite_superior

        slot_h = THUMB_SIZE[1] + 2 * PADDING
        espacio_entre_slots = 18
        espacio_total = slot_h + espacio_entre_slots

        total_altura_slots = len(saves) * espacio_total
        max_scroll = max(0, total_altura_slots - zona_scroll_altura)

        # Scroll animado más fluido
        SCROLL_SPEED = 0.08
        scroll_offset += (scroll_target - scroll_offset) * SCROLL_SPEED

        start_y = limite_superior
        ancho_slot = ANCHO - 200
        x_slot = 100

        # ================================
        # CLIPPING (solo dibujar dentro del área)
        # ================================
        clip_rect = pygame.Rect(0, limite_superior, ANCHO, zona_scroll_altura)
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
                fecha_bonita = fecha[8:10] + "/" + fecha[5:7] + "/" + fecha[:4] + " – " + fecha[11:16]
            except:
                fecha_bonita = fecha

            txt = fuente.render(fecha_bonita, True, AZUL)
            ventana.blit(
                txt,
                (boton.rect.x + THUMB_SIZE[0] + 24,
                 boton.rect.y + boton.rect.height // 2 - txt.get_height() // 2)
            )

        # Restablecer área de dibujo normal
        ventana.set_clip(None)

        # ================================
        # MENSAJE SI NO HAY PARTIDAS
        # ================================
        if len(saves) == 0:
            txt = fuente.render("No hay partidas guardadas", True, AZUL)
            ventana.blit(txt, (ANCHO // 2 - txt.get_width() // 2, ALTO // 2))

        # ================================
        # BOTÓN VOLVER
        # ================================
        boton_volver = Boton(ANCHO // 2 - 100, ALTO - 80, 200, 50, "Volver", CREMA, AZUL, fuente)
        boton_volver.dibujar(ventana, mouse_pos)

        pygame.display.update()
        clock.tick(60)
