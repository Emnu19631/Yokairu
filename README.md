# YOKAIRYU — Novela Visual en Pygame

YOKAIRYU es una novela visual interactiva desarrollada en **Python** usando **Pygame**.  
Incluye un sistema de decisiones, guardado de partida, música ambiental y una interfaz de ajustes para pantalla completa y volumen.

---

## Estructura del Proyecto

```text
yoka/
│
├── assets/
│   ├── audio/                # Archivos de sonido y música
│   └── images/               # Imágenes y fondos del juego
│
├── saves/
│   └── savegame.json         # Archivo de guardado automático
│
├── src/
│   ├── core/
│   │   ├── config.py         # Configuración general del juego
│   │   └── render.py         # Sistema de renderizado de texto con efecto de tipeo
│   │
│   ├── ui/
│   │   ├── boton.py          # Clase de botones interactivos
│   │   ├── ajustes.py        # Pantalla de configuración (volumen y pantalla completa)
│   │   └── menu.py           # Menú principal de inicio
│   │
│   ├── game/
│   │   ├── historia.py       # Contiene las escenas y narraciones del juego
│   │   ├── engine.py         # Motor principal de la novela visual
│   │   └── save_system.py    # Sistema de guardado y carga de partida
│   │
│   └── main.py               # Punto de entrada principal
│
└── README.md
