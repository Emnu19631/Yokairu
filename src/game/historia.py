import pygame
from ui.boton import Boton
from core.config import ANCHO, ALTO, cargar_imagen, CREMA, AZUL, BLANCO, AZUL_RESALTADO, PANTALLA_COMPLETA
from core.render import mostrar_texto_tipeado_con_fondo_solido

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================

BACKGROUND_JUEGO = "background_juego.jpg"
BACKGROUND_VOLCAN = "background_volcan.png"
BACKGROUND_NEGRO= "background_negro.jpg"
BACKGROUND_ISLA="background_isla.png"
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
            {"texto": "Al volcán", "next": 11},
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
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Decidí ir al volcán, se veía interesante aunque no parecía tener mucha vida. "
            "pero igualmente decidí probar mi suerte, después de todo necesito ver que  "
            "Eso fue hasta que alguien finalmente se me acercó: "
            "puedo encontrar "
        )
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_VOLCAN,
        
        "texto": (
            "Sin embargo al llegar al volcán solo había destrucción y parecía estar "
            "completamente abandonado pero creí ver algo extraño en una esquina, tal vez  "
            "no era nada y solo era mi imaginacion, aun asi decidi acercarme pero al "
            "hacerlo……"
        ),
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_NEGRO,
        
        "texto": (
            "Todo se torno negro y me parecio escuchar a alguien pero no lograba ver  "
            "mucho, solo una silueta que intente seguir con cuidado para no caerme o"
            "tropezarme con algo al avanzar"
        ),
        "imagen": "Meiro_exe_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            SLIDE_5_01, SLIDE_5_02, SLIDE_5_03,
            SLIDE_5_04, SLIDE_5_05, SLIDE_5_06, SLIDE_5_07
        ],
        "texto": (
            "Aquella figura dijo “tu no deberias estar aqui” y despues de eso apareci en "
            "donde estaba al inicio pero había un pequeño detalle, el lugar, si bien era el "
            "mismo se veía distinto"
        ),
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Ahora el volcán ya no estaba, era como si hubiera sido borrado  "
            "completamente o algo parecido así que ahora solo podía ir al pueblo, prado"
            "o la isla"
        ),
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Entonces, a dónde iré ahora?"
        ),
    },
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "texto": "",
        "layout": "2x2",
        "opciones": [
            {"texto": "Al pueblo", "next": 4},
            {"texto": "A la isla", "next": 18},
            {"texto": "Al prado", "next": None},
        ],
    },
    { "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "La isla se veía demasiado interesante al estar hecha de hielo además de que  "
            "me pareció ver un oso polar por allí por lo que fui a explorar la misma  "
            "tranquilamente, mientras caminaba alguien se me acercó aunque desconocía si "
            "era hombre o mujer"
        ),
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Oh! Hola, soy Lapi Minato, un tiburón y rey del mar Diamonds Blue, es un  "
            "placer conocerte mi estimada, por lo visto necesitas algo de ayuda, no es"
            "así?"
        ),
        "imagen": "Lapi_a.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Así que Lapi, interesante, suena como lápiz, es gracioso, y qué más dijo? rey  "
            "del mar? entonces es un chico? bueno, yo no juzgo pero se ve algo femenino "
            "aunque me gusta su estilo sinceramente, tal vez debería preguntarle algo sobre "
            "este lugar"
        ),
        "imagen": "Lapi_b.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Entonces, hay algo que te gustaría saber sobre este lugar?"
        ),
        "imagen": "Lapi_b.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Entonces, hay algo que te gustaría saber sobre este lugar?"
        ),
        "imagen": "Lapi_b.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_ISLA,
        "imagen": "Lapi_c.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "opciones": [
            {"texto": "No pareces un tiburón", "next": 24},
            {"texto": "Vives en el mar?", "next": 24},
        ],
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Ese es un secreto que no revelaré por ahora pero te prometo que algún"
            "día lo sabrás"
        ),
        "imagen": "Lapi_d.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Y hablando de secretos, hay algo que debo mostrarte y alguien que quiere presentarse"
            "Mencionó para luego de eso tomar mi mano y llevarme con él a conocer a aquella persona"
            "misteriosa"
        ),
        "imagen": "Lapi_d.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Si, soy un tiburón y vivo en el mar pero ahí veces que me gusta estar en"
            "la tierra para hacer ciertas cosas que no revelaré"
        ),
        "imagen": "Lapi_e.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
]