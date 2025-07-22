# game/config.py

# --- Configuración de la Ventana ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "La Fuga de Jioqué"

# --- Colores (usando valores RGB o CSS de Arcade si son muy comunes) ---
# Puedes usar los colores CSS de Arcade directamente, o definir los tuyos propios en RGB
# Ejemplo RGB:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# --- Configuración del Jugador (Jioqué) ---
# Puedes mover esto aquí para que sea fácil de ajustar
JIOQUE_SCALE = 0.5 # Escala del sprite (0.5 significa 50% del tamaño original)
JIOQUE_START_X = SCREEN_WIDTH / 2
JIOQUE_START_Y = SCREEN_HEIGHT / 2
JIOQUE_MOVEMENT_SPEED = 5 # Velocidad de movimiento en píxeles por actualización

# --- Configuración de Enemigos (Catman, Batwoman) ---
ENEMY_SCALE = 0.7
CATMAN_SPEED = 3
BATWOMAN_SPEED = 4

# --- Otras configuraciones ---
GRAVITY = 0.5 # Fuerza de la gravedad (si tu juego la usa)

# --- Configuración de Música ---
# Lista de rutas a sus archivos de música
# IMPORTANTE: Reemplacen estas rutas con las rutas reales a sus archivos de sonido (por ejemplo, .mp3, .wav)
# Asegúrense de que los archivos existan en estas ubicaciones dentro de su carpeta 'assets/sounds/'.
MUSIC_LIST = [
    "assets/sounds/music/1.mp3", # Ejemplo: reemplazar con "assets/sounds/mi_cancion_favorita.mp3"
    "assets/sounds/music/2.mp3", # Ejemplo: reemplazar con "assets/sounds/musica_fondo.wav"
    "assets/sounds/music/3.mp3"  # Ejemplo: reemplazar con "assets/sounds/tema_principal.ogg"
]
