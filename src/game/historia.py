import pygame
from ui.boton import Boton
from core.config import ANCHO, ALTO, cargar_imagen, CREMA, AZUL, BLANCO, AZUL_RESALTADO, PANTALLA_COMPLETA
from core.render import mostrar_texto_tipeado_con_fondo_solido

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BACKGROUND_JUEGO = "background_juego.jpg"
SLIDE_5_01 = "slide5-01.jpg"
SLIDE_5_02 = "slide5-02.jpg"
SLIDE_5_03 = "slide5-03.jpg"
SLIDE_5_04 = "slide5-04.jpg"
SLIDE_5_05 = "slide5-05.jpg"
SLIDE_5_06 = "slide5-06.jpg"
SLIDE_5_07 = "slide5-07.jpg"

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
            {"texto": "A la isla", "next": None},
            {"texto": "Al prado", "next": None},
            {"texto": "Al volcán", "next": None},
        ],
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            SLIDE_5_01, SLIDE_5_02, SLIDE_5_03,
            SLIDE_5_04, SLIDE_5_05, SLIDE_5_06, SLIDE_5_07
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
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            SLIDE_5_01, SLIDE_5_02, SLIDE_5_03,
            SLIDE_5_04, SLIDE_5_05, SLIDE_5_06, SLIDE_5_07
        ],
        "texto": (
            "(Así que la persona frente a mí se llamaba Rayco, era bueno saber eso. "
            "Ahora podría responder algunas de mis dudas... ¿con qué debería comenzar?)"
        ),
        "imagen": "rayco_oc.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "opciones": [
            {"texto": "¿Dónde estamos?", "next": 7},
            {"texto": "¿Cómo regreso a mi casa?", "next": 9},
        ],
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "¿Con que quieres saber dónde estamos o qué es este lugar? Bueno, estamos en Yokairyu. "
            "Este es un mundo especial, aquí existe la magia y hay mucho por explorar. "
            "Sí, sé lo que estás pensando... ¿no se supone que Yokairyu es un juego? "
            "Pues sí, pero también es otro mundo, un mundo algo…"
        ),
        "imagen": "rayco_oa.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Especial. Descuida, con el tiempo te vas a acostumbrar a este lugar, te lo prometo. "
            "A mí también me costó un poco al principio, pero mi jefa me ayudó. "
            "De hecho, te voy a llevar con ella, vamos. "
            "(Luego de eso, agarró mi mano y me llevó con él.)"
        ),
        "imagen": "rayco_estr.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "next": 10
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            SLIDE_5_01, SLIDE_5_02, SLIDE_5_03,
            SLIDE_5_04, SLIDE_5_05, SLIDE_5_06, SLIDE_5_07
        ],
        "texto": (
            "¿Regresar a tu casa? Eso es algo complicado... no sabría decirte cómo hacerlo, "
            "pero mi jefa puede ayudarte. Vamos, te llevaré con ella. "
            "(Dijo y empezamos a caminar por el pueblo en busca de su jefa.)"
        ),
        "imagen": "rayco_oc.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "(Después de un rato caminando con Rayco llegamos con "
            "una chica que por algún motivo se me hacia conocida "
            "aunque probablemente solo era mi imaginacion)"
        ),
    },
]
