# game/player.py

import arcade
from game.config import JIOQUE_SCALE, JIOQUE_MOVEMENT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

# Ruta a la imagen de Jioqué (ajusta si el nombre del archivo es diferente)
PLAYER_IMAGE = "assets/images/player/jioque_sprite.png"

class Player(arcade.Sprite):
    """
    Clase que representa a Jioqué (el jugador).
    """
    def __init__(self):
        """
        Constructor de la clase Player.
        """
        # Llama al constructor de la clase arcade.Sprite
        # Esto carga la imagen y le aplica una escala
        super().__init__(PLAYER_IMAGE, JIOQUE_SCALE)

        # Establece la posición inicial de Jioqué
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

        # Guarda la velocidad de movimiento para usarla más tarde
        self.speed = JIOQUE_MOVEMENT_SPEED

    def update(self):
        """
        Aquí es donde implementaremos el movimiento más adelante.
        """
        # Por ahora, Jioqué no se mueve automáticamente.
        # Su movimiento será controlado por el teclado en main.py
        pass

    # Más adelante, aquí añadirás métodos para saltar, atacar, etc.