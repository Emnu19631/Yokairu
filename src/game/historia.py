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
BACKGROUND_PRADO="fondo_prado.png"
BACKGROUND_ESTRELLA="fondo_estrella.png"
BACKGROUND_FINAL="fondo_fin.png"
SLIDE_5_01 = "slide5-01.jpg"
SLIDE_5_02 = "slide5-02.jpg"
SLIDE_5_03 = "slide5-03.jpg"
SLIDE_5_04 = "slide5-04.jpg"
SLIDE_5_05 = "slide5-05.jpg"
SLIDE_5_06 = "slide5-06.jpg"
SLIDE_5_07 = "slide5-07.jpg"
MEIRO_IMG = "Meiro_exe.png"
MEIROB_IMG = "meirob.png"

# ===============================
# HISTORIA PRINCIPAL
# ===============================

HISTORIA = [
    #0
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
    #1
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
    #2
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
    #3
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "texto": "",
        "layout": "2x2",
        "opciones": [
            {"texto": "Al pueblo", "next": 4},
            {"texto": "A la isla", "next": 18},
            {"texto": "Al prado", "next": 32},
            {"texto": "Al volcán", "next": 11},
        ],
    },
    #4
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
    #5
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
    #6
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
    #7
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
    #8
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
    #9
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
    #10
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "(Después de un rato caminando con Rayco llegamos con "
            "una chica que por algún motivo se me hacia conocida "
            "aunque probablemente solo era mi imaginacion)"
        ),
        "next": 27
    },
    #11
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
    #12
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
    #13
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
    #14
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
    #15
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Ahora el volcán ya no estaba, era como si hubiera sido borrado  "
            "completamente o algo parecido así que ahora solo podía ir al pueblo, prado"
            "o la isla"
        ),
    },
    #16
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Entonces, a dónde iré ahora?"
        ),
    },
    #17
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_JUEGO,
        "texto": "",
        "layout": "2x2",
        "opciones": [
            {"texto": "Al pueblo", "next": 4},
            {"texto": "A la isla", "next": 18},
            {"texto": "Al prado", "next": 32},
        ],
    },
    #18
    { "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "La isla se veía demasiado interesante al estar hecha de hielo además de que  "
            "me pareció ver un oso polar por allí por lo que fui a explorar la misma  "
            "tranquilamente, mientras caminaba alguien se me acercó aunque desconocía si "
            "era hombre o mujer"
        ),
    },
    #19
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
    #20
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
    #21
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
    #22
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_ISLA,
        "imagen": "Lapi_c.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "opciones": [
            {"texto": "No pareces un tiburón", "next": 25},
            {"texto": "Vives en el mar?", "next": 23},
        ],
    },
    #23
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
    #24
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
        "pos_rel": (0.35, 0.15),
        "next": 27
    },
    #25
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
    #26
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ISLA,
        
        "texto": (
            "Te presentare a alguien muy especial para mí"
            "Sigueme!!!"
        ),
        "imagen": "Lapi_e.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #27
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        
        "texto": (
            "Buenas tardes, soy Meiro Exe, yo fui quien te trajo aquí"
            "se que es muy repentino pero confía en mí, estás a salvo aquí"
        ),
        "imagen": MEIRO_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #28
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        
        "texto": (
            "Quiero sabes si quieres irte a casa o quedarte aquí conmigo"
        ),
        "imagen": MEIRO_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #29
    {
        "tipo": "eleccion",
        "fondo": BACKGROUND_ESTRELLA,
        "imagen": MEIRO_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "opciones": [
            {"texto": "Quiero ir a casa", "next": 30},
            {"texto": "Quiero quedarme", "next": 42},
        ],
    },
    #30
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        
        "texto": (
            "Entiendo, si ese es tu deseo, te ayudaré a regresar a casa"
            "Solo confía en mí"
        ),
        "imagen": MEIRO_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15),
        "next": 45
    },
    #31
    { "tipo": "narracion",
        "fondo": BACKGROUND_FINAL,
        
        "texto": (
            ".  "
        ),
    },
    #32
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "El prado se veía lindo ademas de que por lo visto corría una brisa agradable  "
            "en el mismo por lo que decidí ir allá, mientras exploraba un poco un chico de"
            "lentes se me acercó"
        ),
        "imagen": "edrian_silueta.png",
        "scalar": 0.5,
        "pos_rel": (0.35, 0.2)
    },
    #33
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "Hola, veo que eres nueva por aqui, me llamo Edrian y por lo visto estas "
            "demasiado confundida, descuida, a todos nos paso lo mismo cuando "
            "llegamos aquí, quieres preguntarme algo?"
        ),
        "imagen": "edrian_silueta.png",
        "scalar": 0.5,
        "pos_rel": (0.35, 0.2)
    },
    #34
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "El prado se veía lindo ademas de que por lo visto corría una brisa agradable  "
            "en el mismo por lo que decidí ir allá, mientras exploraba un poco un chico de"
            "lentes se me acercó"
        ),
        "imagen": "Edrian.png",
        "scalar": 0.3,
        "pos_rel": (0.30, 0.1)
    },
    #35
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "Entonces Edrian, ese es un nombre interesante, veamos, qué podría preguntarle? "
        ),
        "imagen": "Edrian.png",
        "scalar": 0.3,
        "pos_rel": (0.30, 0.1)
    },
    #36
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "Lapi, es bueno verte aunque sabia que vendrias, en fin, ella debe ser la nueva, "
            "es un placer, me llamo Meiro y te contaré algunas cosas sobre este lugar que "
            "podrían serte de ayuda más adelante, empecemos, si?"
        ),
        "imagen": "meiroc_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.37, 0.2)
    },
    #37
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_PRADO,
        "texto": (
            "Para empezar, el motivo por el que estás aquí es porque……  "
            "Porque yo lo quise así querida, simplemente por eso "
            "(Su voz había cambiado, se escuchaba algo distorsionada)"
        ),
        "imagen": MEIROB_IMG,
        "scalar": 0.2,
        "pos_rel": (0.33, 0.2)
    },
    #38
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        "texto": (
            "Apareció una chica frente a mi y el lugar cambio, esta chica se veía como la anterior pero "
            "también lucía diferente, me daba algo de miedo sinceramente "
            "Bueno, como dije, estás aquí porque yo quiero que estes aqui y no podrás irte a ninguna "
            "parte, ahora eres mi nueva diversión, yo soy Meiro.exe por cierto"
        ),
        "imagen": "Meiro_exe_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #39
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        "texto": (
            "Oh vamos, no tienes porque ponerte asi, despues de todo vas a terminar "
            "olvidando tu vida y pensarás que siempre has vivido aquí, en unos días eso "
            "pasara, por ahora, te deseo suerte buscando una salida aunque se que no la "
            "encontraras pero será divertido verte intentarlo"
        ),
        "imagen": MEIRO_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #40
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        "texto": (
            "Rayco, sabia que vendrias, y ella, supuse que llegaría a mi tarde o temprano, ahora  "
            "dime, quieres irte de este lugar, no es así? oh, pero que maleducada soy, me llamo "
            "Meiro, en cuanto a mi pregunta, dime, quieres regresar a casa"
        ),
        "imagen": "meiroc_silueta.png",
        "scalar": 0.4,
        "pos_rel": (0.37, 0.2)
    },
    #41
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_ESTRELLA,
        "texto": (
            "Rayco, veo que traes a una pequeña que quiere irse a su casa, bueno, dejame "
            "decir que eso no se puede, no lo pienso permitir, te quedaras aquí igual que "
            "todos los demás, descuida, con el tiempo vas a olvidar quién fuiste y tu “hogar”,"
            "oh vamos, no pongas esa cara, esta aventura será divertida"
        ),
        "imagen": "meiroc.png",
        "scalar": 0.6,
        "pos_rel": (0.37, 0.2),
        "next": 45
    },
    #42
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Me alegro de que quieras quedarte aquí! Rayco te mostrará  "
            "qué más puedes dominar, buena suerte"
        ),
        "imagen": MEIROB_IMG,
        "scalar": 0.2,
        "pos_rel": (0.35, 0.2),
        "next": 45
    },
    #43
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "texto": (
            "Con que quieres irte, bueno, dejame decirte algo, no puedes irte si yo no  "
            "quiero que te vayas y no te dejaré escapar, verás, es muy aburrido este"
            "lugar así que te quedaras aqui y seras parte de mi diversión junto a los"
            "otros y no intentes protestar o escapar….."
        ),
        "imagen": MEIROB_IMG,
        "scalar": 0.4,
        "pos_rel": (0.35, 0.15)
    },
    #44
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_JUEGO,
        "transicion_fondos": [
            SLIDE_5_01, SLIDE_5_02, SLIDE_5_03,
            SLIDE_5_04, SLIDE_5_05, SLIDE_5_06, SLIDE_5_07
        ],
        "texto": (
            "Te lo diré de una manera muy sencilla para que tu pequeña cabecita  "
            "humana logre entenderlo, ahora podras salir de aqui"
        ),
    },
    #45
    {
        "tipo": "narracion",
        "fondo": BACKGROUND_FINAL,
        "texto": (
            "."
        ),
    },
]
