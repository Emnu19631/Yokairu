import pygame
from config import ANCHO, ALTO
from novela_visual import ejecutar_novela # <--- IMPORTACIÓN CLAVE

# ===============================
# FUNCIÓN INICIAR PARTIDA
# ===============================
def iniciar_partida(ventana, ancho, alto, fuente):
    """
    Función principal para la secuencia de inicio de la novela visual.
    Llama a la función que ejecuta las slides de la historia.
    """
    # Llama al motor de la novela visual
    resultado = ejecutar_novela(ventana, fuente) # <--- LLAMADA AL NUEVO MOTOR
    
    # Maneja la acción de salida si el usuario cerró la ventana durante la novela
    if resultado == "salir":
        return "salir" 
    
    return "menu" # Vuelve al menú principal al terminar la secuencia