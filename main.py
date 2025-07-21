import arcade
# Importamos todas las configuraciones necesarias de game.config
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BLACK # Asegúrate de que BLACK también esté en tu config.py
from game.player import Player

class MyGame(arcade.Window):
    """
    Clase principal del juego.
    """

    def __init__(self, width, height, title):
        """
        Constructor de la clase MyGame.
        Se llama una vez al inicio del juego.
        """
        super().__init__(width, height, title)

        # Establece el color de fondo de la ventana usando la configuración
        arcade.set_background_color(BLACK)

        # --- Crear una instancia de Jioqué ---
        # Asegúrate de que esta línea esté presente para crear a Jioqué
        self.player_sprite = Player()


    def on_draw(self):
        """
        Se llama cada vez que necesitamos redibujar la pantalla.
        """
        self.clear() # Limpia la pantalla para el nuevo fotograma

        # --- Dibujar a Jioqué ---
        self.player_sprite.draw()

        # Puedes dibujar texto o formas si quieres
        arcade.draw_text("¡La Fuga de Jioqué!", 10, 10, arcade.csscolor.WHITE, 20)


    def update(self, delta_time):
        """
        Se llama para actualizar la lógica del juego (movimiento, colisiones, etc.).
        """
        # Llama al metodo update() de tu objeto Player para que se mueva
        self.player_sprite.update()
        pass

def main():
    """
    Función principal para ejecutar el juego.
    """
    # Usa las variables importadas de game.config
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run() # Inicia el bucle principal del juego

if __name__ == "__main__":
    main() # Ejecuta la función principal si el script se ejecuta directamente