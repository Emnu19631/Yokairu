# test_menu.py
import pytest
import pygame
from unittest.mock import patch
import ui.menu as main  # <- aquí apuntamos al módulo correcto

pygame.init()

# ===============================
# Mocks para funciones externas
# ===============================

@patch("ui.menu.ejecutar_novela", return_value=None)
@patch("ui.menu.pantalla_ajustes", return_value="salir")
@patch("ui.menu.pantalla_cargar", return_value=None)
@patch("ui.menu.cargar_partida_por_id", return_value={"slide": 0})
def test_mouse_interactions(mock_cargar, mock_cargar_pantalla, mock_ajustes, mock_novela):
    # Creamos botones de prueba
    main.botones = main.crear_botones()
    
    # ===============================
    # Simulación de MOUSEMOTION
    # ===============================
    for i, boton in enumerate(main.botones):
        evento_motion = pygame.event.Event(pygame.MOUSEMOTION, {"pos": boton.rect.center})
        main.indice_seleccionado = -1
        for evento in [evento_motion]:
            if evento.type == pygame.MOUSEMOTION:
                for j, b in enumerate(main.botones):
                    if b.rect.collidepoint(evento.pos):
                        main.indice_seleccionado = j
                        break
        assert main.indice_seleccionado == i
    
    # ===============================
    # Simulación de MOUSEBUTTONDOWN
    # ===============================
    for i, boton in enumerate(main.botones):
        evento_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": boton.rect.center, "button": 1})
        main.corriendo = True
        with patch("pygame.display.update"), patch("pygame.mixer.music.stop"):
            for evento in [evento_click]:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for j, b in enumerate(main.botones):
                        if b.es_click(evento.pos):
                            main.indice_seleccionado = j
                            texto = b.texto
                            if texto == "Salir":
                                main.corriendo = False
                            elif texto == "Iniciar":
                                main.engine.id_actual_save = None
                                estado = "historia:0"
                                continuar = True
                                while continuar and estado.startswith("historia"):
                                    resultado = main.ejecutar_novela(main.ventana, main.fuente, main.ANCHO, main.ALTO, 0)
                                    if resultado == "salir":
                                        main.corriendo = False
                                        continuar = False
                                    else:
                                        continuar = False
                            elif texto == "Cargar":
                                seleccionado = main.pantalla_cargar(main.fuente)
                                if seleccionado is not None:
                                    main.engine.id_actual_save = seleccionado
                                    slot = main.cargar_partida_por_id(seleccionado)
                                    slide_guardado = int(slot.get("slide", 0)) if slot else 0
                                    estado = f"historia:{slide_guardado}"
                                    continuar = True
                                    while continuar and estado.startswith("historia"):
                                        resultado = main.ejecutar_novela(main.ventana, main.fuente, main.ANCHO, main.ALTO, slide_guardado)
                                        if resultado == "salir":
                                            main.corriendo = False
                                            continuar = False
                                        else:
                                            continuar = False
                            elif texto == "Ajustes":
                                resultado = main.pantalla_ajustes(main.fuente)
                                accion = resultado if not isinstance(resultado, tuple) else resultado[0]
                                if accion == "salir":
                                    main.corriendo = False
        # Verificamos que el flujo cambie corriendo a False al clicar salir o ajustes->salir
        if boton.texto in ["Salir", "Ajustes"]:
            assert main.corriendo is False
        else:
            assert main.corriendo is True


# ===============================
# Tests adicionales para cubrir cada opción
# ===============================

@patch("ui.menu.ejecutar_novela", return_value="historia:0")
@patch("ui.menu.pantalla_ajustes", return_value="continuar")
def test_boton_iniciar(mock_ajustes, mock_novela):
    main.botones = [b for b in main.crear_botones() if b.texto == "Iniciar"]
    main.corriendo = True
    boton = main.botones[0]

    evento_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": boton.rect.center, "button": 1})
    for evento in [evento_click]:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for j, b in enumerate(main.botones):
                if b.es_click(evento.pos):
                    texto = b.texto
                    if texto == "Iniciar":
                        main.engine.id_actual_save = None
                        estado = "historia:0"
                        continuar = True
                        while continuar and estado.startswith("historia"):
                            resultado = main.ejecutar_novela(main.ventana, main.fuente, main.ANCHO, main.ALTO, 0)
                            if resultado == "salir":
                                main.corriendo = False
                                continuar = False
                            else:
                                continuar = False
    assert main.corriendo is True

@patch("ui.menu.pantalla_cargar", return_value=1)
@patch("ui.menu.cargar_partida_por_id", return_value={"slide": 2})
@patch("ui.menu.ejecutar_novela", return_value="historia:2")
def test_boton_cargar(mock_novela, mock_cargar, mock_pantalla):
    main.botones = [b for b in main.crear_botones() if b.texto == "Cargar"]
    main.corriendo = True
    boton = main.botones[0]

    evento_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": boton.rect.center, "button": 1})
    for evento in [evento_click]:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for j, b in enumerate(main.botones):
                if b.es_click(evento.pos):
                    texto = b.texto
                    if texto == "Cargar":
                        seleccionado = main.pantalla_cargar(main.fuente)
                        if seleccionado is not None:
                            main.engine.id_actual_save = seleccionado
                            slot = main.cargar_partida_por_id(seleccionado)
                            slide_guardado = int(slot.get("slide", 0)) if slot else 0
                            estado = f"historia:{slide_guardado}"
                            continuar = True
                            while continuar and estado.startswith("historia"):
                                resultado = main.ejecutar_novela(main.ventana, main.fuente, main.ANCHO, main.ALTO, slide_guardado)
                                if resultado == "salir":
                                    main.corriendo = False
                                    continuar = False
                                else:
                                    continuar = False
    assert main.corriendo is True

@patch("ui.menu.pantalla_ajustes", return_value="salir")
def test_boton_ajustes(mock_ajustes):
    main.botones = [b for b in main.crear_botones() if b.texto == "Ajustes"]
    main.corriendo = True
    boton = main.botones[0]

    evento_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": boton.rect.center, "button": 1})
    for evento in [evento_click]:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for j, b in enumerate(main.botones):
                if b.es_click(evento.pos):
                    texto = b.texto
                    if texto == "Ajustes":
                        resultado = main.pantalla_ajustes(main.fuente)
                        accion = resultado if not isinstance(resultado, tuple) else resultado[0]
                        if accion == "salir":
                            main.corriendo = False
    assert main.corriendo is False