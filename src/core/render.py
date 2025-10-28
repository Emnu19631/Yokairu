import pygame

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

def dividir_texto_en_lineas(texto, fuente, max_ancho):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        prueba_linea = linea_actual + ("" if linea_actual == "" else " ") + palabra
        ancho, _ = fuente.size(prueba_linea)
        if ancho <= max_ancho:
            linea_actual = prueba_linea
        else:
            if linea_actual != "":
                lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return lineas

# ===============================
# AJUSTE DE FUENTE
# ===============================

def ajustar_fuente_al_rect(texto, fuente_inicial, rect):
    tamano_fuente = fuente_inicial.get_height()
    nombre_fuente = fuente_inicial.get_name() if hasattr(fuente_inicial, "get_name") else None
    max_ancho = rect.width - 20
    max_alto = rect.height - 20
    while tamano_fuente > 10:
        if nombre_fuente:
            fuente = pygame.font.Font(nombre_fuente, tamano_fuente)
        else:
            fuente = pygame.font.SysFont(None, tamano_fuente)
        lineas = dividir_texto_en_lineas(texto, fuente, max_ancho)
        altura_total = len(lineas) * (fuente.get_height() + 2)
        if altura_total <= max_alto:
            return fuente, lineas
        tamano_fuente -= 1
    if nombre_fuente:
        fuente = pygame.font.Font(nombre_fuente, tamano_fuente)
    else:
        fuente = pygame.font.SysFont(None, tamano_fuente)
    lineas = dividir_texto_en_lineas(texto, fuente, max_ancho)
    return fuente, lineas

# ===============================
# EFECTO DE TIPEO
# ===============================

def mostrar_texto_tipeado_con_fondo_solido(ventana, fuente_inicial, texto, color, rect, velocidad=50):
    reloj = pygame.time.Clock()
    indice, texto_mostrado = 0, ""
    tiempo_ultimo = pygame.time.get_ticks()
    while indice < len(texto):
        if _verificar_salida_eventos():
            return True
        texto_mostrado, indice, tiempo_ultimo = _actualizar_texto_tipeado(
            texto, texto_mostrado, indice, tiempo_ultimo, velocidad
        )
        _dibujar_texto_tipeado(ventana, fuente_inicial, texto_mostrado, color, rect)
        reloj.tick(60)
    _esperar_confirmacion_usuario(reloj)
    return False

# ===============================
# EVENTOS DE SALIDA
# ===============================

def _verificar_salida_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return True
        if _es_evento_de_salida(evento):
            return True
    return False

def _es_evento_de_salida(evento):
    return (
        evento.type == pygame.MOUSEBUTTONDOWN
        or (evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE))
    )

# ===============================
# ACTUALIZACIÓN Y DIBUJO
# ===============================

def _actualizar_texto_tipeado(texto, texto_mostrado, indice, tiempo_ultimo, velocidad):
    tiempo_actual = pygame.time.get_ticks()
    if indice < len(texto) and tiempo_actual - tiempo_ultimo > velocidad:
        texto_mostrado += texto[indice]
        indice += 1
        tiempo_ultimo = tiempo_actual
    return texto_mostrado, indice, tiempo_ultimo

def _dibujar_texto_tipeado(ventana, fuente_inicial, texto_mostrado, color, rect):
    ventana.fill((234, 210, 146), rect)
    fuente_ajustada, lineas = ajustar_fuente_al_rect(texto_mostrado, fuente_inicial, rect)
    y = rect.y + 10
    for linea in lineas:
        render = fuente_ajustada.render(linea, True, color)
        ventana.blit(render, (rect.x + 10, y))
        y += fuente_ajustada.get_height() + 2
    pygame.display.update()

# ===============================
# CONFIRMACIÓN DEL USUARIO
# ===============================

def _esperar_confirmacion_usuario(reloj):
    while True:
        if _verificar_salida_eventos():
            break
        reloj.tick(60)
