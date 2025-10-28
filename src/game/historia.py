import pygame
from ui.boton import Boton
from core.config import ANCHO, ALTO, cargar_imagen, CREMA, AZUL, BLANCO, AZUL_RESALTADO, PANTALLA_COMPLETA
from core.render import mostrar_texto_tipeado_con_fondo_solido

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BACKGROUND_JUEGO = "background_juego.jpg"

# ===============================
# HISTORIA PRINCIPAL
# ===============================

HISTORIA = [
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Hola mi querido jugador! ¿Qué tal estás? Claramente estás algo perdido o no estarías aquí, "
            "aunque sinceramente no sé para qué necesitas un tutorial para este juego..."
        ),
        "imagen": "meiro.png",
        "scalar": 0.25,
        "pos_rel": (0.13, 0.05)
    },
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Antes de empezar con el juego, por favor selecciona si eres hombre o mujer "
            "para que la historia se adapte mejor a ti."
        ),
        "opciones": [
            {"texto": "Hombre", "next": 2},
            {"texto": "Mujer", "next": 2},
        ],
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Había despertado en un lugar extraño que no conocía, lo último que recordaba era que estaba "
            "jugando en mi computadora, de repente una luz cegadora y luego de eso este lugar desconocido. "
            "Es extraño... ¿acaso había sido secuestrada por el juego o algo parecido? No lo sabía. "
            "Tal vez, para empezar, sería buena idea pedir ayuda o preguntar algunas cosas."
        ),
    },
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "texto": "",
        "layout": "2x2",
        "opciones": [
            {"texto": "Al pueblo", "next": 4},
            {"texto": "A la isla", "next": 5},
            {"texto": "Al prado", "next": 6},
            {"texto": "Al volcán", "next": 7},
        ],
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            "slide5-01.jpg", "slide5-02.jpg", "slide5-03.jpg",
            "slide5-04.jpg", "slide5-05.jpg", "slide5-06.jpg", "slide5-07.jpg"
        ],
        "texto": (
            "Decidí ir al pueblo, supuse que allí encontraría mucha gente a la cual pedirle ayuda. "
            "Y sí, había gente, pero nadie parecía verme... o si lo hacían, me ignoraban completamente. "
            "Eso fue hasta que alguien finalmente se me acercó: "
            "una especie de conejo con ropas de color café. Interesante... "
            "tal vez él estaba a cargo."
        )
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Hola! Veo que estás un poco perdida, necesitas ayuda? "
            "Y lo siento por la gente de aquí, a mi tampoco me hacen caso sinceramente, "
            "oh, me llamo Rayco por cierto, es un placer"
        ),
        "imagen": "rayco_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            "slide5-01.jpg", "slide5-02.jpg", "slide5-03.jpg",
            "slide5-04.jpg", "slide5-05.jpg", "slide5-06.jpg", "slide5-07.jpg"
        ],
        "texto": (
            "Hola! Veo que estás un poco perdida, necesitas ayuda? "
            "Y lo siento por la gente de aquí, a mi tampoco me hacen caso sinceramente, "
            "oh, me llamo Rayco por cierto, es un placer"
        ),
        "imagen": "rayco_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    }
]
