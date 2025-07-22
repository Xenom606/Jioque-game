import arcade
import arcade.gui
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UITextureButton
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MUSIC_LIST
from game.player import Player
from game.music_player import MusicPlayer

class GameView(arcade.View):
    """
    Vista principal del juego.
    """
    def __init__(self, window, music_player):
        super().__init__(window)
        self.player_sprite_list = arcade.SpriteList()
        self.info_text = None
        self.music_player = music_player
        self.background_texture = arcade.load_texture("assets/images/backgrounds/main.png")

        self.ui_manager = UIManager(self.window)
        self._setup_music_controls()

    def _setup_music_controls(self):
        box = UIBoxLayout(vertical=False, space_between=10)

        # Botones de navegación
        prev_button = UITextureButton(
            texture=arcade.load_texture("assets/images/ui/left.png"),
            texture_hovered=arcade.load_texture("assets/images/ui/left_hover.png"),
            texture_pressed=arcade.load_texture("assets/images/ui/left_pressed.png"),
        )
        prev_button.on_click = lambda _: self.music_player.previous_song()
        prev_button.scale(0.25)
        box.add(prev_button)

        next_button = UITextureButton(
            texture=arcade.load_texture("assets/images/ui/right.png"),
            texture_hovered=arcade.load_texture("assets/images/ui/right_hover.png"),
            texture_pressed=arcade.load_texture("assets/images/ui/right_pressed.png"),
        )
        next_button.on_click = lambda _: self.music_player.next_song()
        next_button.scale(0.25)
        box.add(next_button)

        # Botón de sonido
        self.normal_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on.png")
        self.hover_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on_hover.png")
        self.press_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on_pressed.png")

        self.normal_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off.png")
        self.hover_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off_hover.png")
        self.press_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off_pressed.png")

        self.mute_button = UITextureButton(
            texture=self.normal_texture_mute_on,
            texture_hovered=self.hover_texture_mute_on,
            texture_pressed=self.press_texture_mute_on,
        )
        self.mute_button.on_click = lambda _: self.music_player.toggle_mute()
        self.mute_button.scale(0.25)
        box.add(self.mute_button)

        self.ui_manager.add(
            UIAnchorLayout(
                anchor_x="right",
                anchor_y="top",
                padding_right=20,
                padding_top=20,
                children=[box]
            )
        )

    def _update_music_button_textures(self):
        if self.music_player.is_muted:
            self.mute_button.texture = self.normal_texture_mute_off
            self.mute_button.texture_hovered = self.hover_texture_mute_off
            self.mute_button.texture_pressed = self.press_texture_mute_off
        else:
            self.mute_button.texture = self.normal_texture_mute_on
            self.mute_button.texture_hovered = self.hover_texture_mute_on
            self.mute_button.texture_pressed = self.press_texture_mute_on

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.ui_manager.enable()
        player = Player()
        player.center_x = SCREEN_WIDTH / 2
        player.center_y = SCREEN_HEIGHT / 2
        self.player_sprite_list.append(player)
        self.info_text = arcade.Text(
            "¡Juego en Progreso!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.8,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

    def on_hide_view(self):
        self.ui_manager.disable()

        def on_draw(self):
            self.clear()
            if self.background_sprite:
                print("Tipo real:", type(self.background_sprite))  # Verifica la clase
                self.background_sprite.draw()
            else:
                print("Fondo no cargado, no se dibuja.")

            if self.background_texture:
                arcade.draw_texture_rectangle(
                    self.window.width // 2,
                    self.window.height // 2,
                    self.window.width,
                    self.window.height,
                    self.background_texture
                )

        # Dibuja los botones del menú principal
        self._draw_button("Empezar el Juego", self.window.width / 2, self.window.height / 2 + 50, 300, 70)
        self._draw_button("Salir", self.window.width / 2, self.window.height / 2 - 40, 300, 70)

        # Dibuja la interfaz de música
        self.ui_manager.draw()
        self._update_music_button_textures()

        # Muestra la canción actual
        arcade.draw_text(
            f"Reproduciendo: {self.music_player.get_current_song_name()}",
            20,
            self.window.height - 30,
            arcade.color.WHITE,
            16
        )

    def on_update(self, delta_time):
        self.player_sprite_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        player = self.player_sprite_list[0]
        if key == arcade.key.LEFT:
            player.change_x = -5
        elif key == arcade.key.RIGHT:
            player.change_x = 5
        elif key == arcade.key.UP:
            player.register_up_press()

    def on_key_release(self, key, modifiers):
        player = self.player_sprite_list[0]
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            player.change_x = 0
        elif key == arcade.key.DOWN:
            player.change_y = 0
        elif key == arcade.key.UP:
            player.up_pressed = False

class MainMenuView(arcade.View):
    """
    Vista del menú principal del juego.
    """

    def __init__(self, window, music_player):
        super().__init__()
        self.window = window
        self.music_player = music_player
        self.mouse_x = 0
        self.mouse_y = 0
        self.ui_manager = arcade.gui.UIManager(self.window)
        self.ui_manager.enable()
        self.background_sprite = arcade.Sprite("assets/images/backgrounds/main.png", scale=1)
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2
        self._setup_music_controls()

    def _setup_music_controls(self):
        """ Configura los botones de control de música para MainMenuView. """
        box = arcade.gui.widgets.layout.UIBoxLayout(vertical=False, space_between=10)

        normal_texture_prev = arcade.load_texture("assets/images/ui/left.png")
        hover_texture_prev = arcade.load_texture("assets/images/ui/left_hover.png")
        press_texture_prev = arcade.load_texture("assets/images/ui/left_pressed.png")

        self.normal_texture_play = arcade.load_texture("assets/images/ui/play.png")
        self.hover_texture_play = arcade.load_texture("assets/images/ui/play_hover.png")
        self.press_texture_play = arcade.load_texture("assets/images/ui/play_pressed.png")

        self.normal_texture_pause = arcade.load_texture("assets/images/ui/pause.png")
        self.hover_texture_pause = arcade.load_texture("assets/images/ui/pause_hover.png")
        self.press_texture_pause = arcade.load_texture("assets/images/ui/pause_pressed.png")

        normal_texture_next = arcade.load_texture("assets/images/ui/right.png")
        hover_texture_next = arcade.load_texture("assets/images/ui/right_hover.png")
        press_texture_next = arcade.load_texture("assets/images/ui/right_pressed.png")

        normal_texture_down = arcade.load_texture("assets/images/ui/down.png")
        hover_texture_down = arcade.load_texture("assets/images/ui/down_hover.png")
        press_texture_down = arcade.load_texture("assets/images/ui/down_pressed.png")

        normal_texture_up = arcade.load_texture("assets/images/ui/up.png")
        hover_texture_up = arcade.load_texture("assets/images/ui/up_hover.png")
        press_texture_up = arcade.load_texture("assets/images/ui/up_pressed.png")

        self.normal_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on.png")
        self.hover_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on_hover.png")
        self.press_texture_mute_on = arcade.load_texture("assets/images/ui/Sound_on_pressed.png")

        self.normal_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off.png")
        self.hover_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off_hover.png")
        self.press_texture_mute_off = arcade.load_texture("assets/images/ui/Sound_off_pressed.png")

        # Botón Canción Anterior
        prev_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=normal_texture_prev,
            texture_hovered=hover_texture_prev,
            texture_pressed=press_texture_prev,
        )
        prev_button.on_click = lambda _: self.music_player.previous_song()
        prev_button.scale(0.25) # Escalado a 25%
        box.add(prev_button)

        # Botón Reproducir/Pausar
        self.play_pause_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=self.normal_texture_play, # Textura inicial
            texture_hovered=self.hover_texture_play,
            texture_pressed=self.press_texture_play,
        )
        self.play_pause_button.on_click = lambda _: self.music_player.play_pause()
        self.play_pause_button.scale(0.25) # Escalado a 25%
        box.add(self.play_pause_button)

        # Botón Canción Siguiente
        next_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=normal_texture_next,
            texture_hovered=hover_texture_next,
            texture_pressed=press_texture_next,
        )
        next_button.on_click = lambda _: self.music_player.next_song()
        next_button.scale(0.25) # Escalado a 25%
        box.add(next_button)

        # Botón Bajar Volumen
        down_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=normal_texture_down,
            texture_hovered=hover_texture_down,
            texture_pressed=press_texture_down,
        )
        down_button.on_click = lambda _: self.music_player.volume_down()
        down_button.scale(0.25) # Escalado a 25%
        box.add(down_button)

        up_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=normal_texture_up,
            texture_hovered=hover_texture_up,
            texture_pressed=press_texture_up,
        )
        up_button.on_click = lambda _: self.music_player.volume_up()
        up_button.scale(0.25) # Escalado a 25%
        box.add(up_button)

        # Botón Silenciar/Activar Sonido
        self.mute_button = arcade.gui.widgets.buttons.UITextureButton(
            texture=self.normal_texture_mute_on, # Textura inicial
            texture_hovered=self.hover_texture_mute_on,
            texture_pressed=self.press_texture_mute_on,
        )
        self.mute_button.on_click = lambda _: self.music_player.toggle_mute()
        self.mute_button.scale(0.25) # Escalado a 25%
        box.add(self.mute_button)
        # Colocar los botones centrados en la parte superior
        self.ui_manager.add(
            arcade.gui.widgets.layout.UIAnchorLayout(
                anchor_x="center_x",
                anchor_y="top",
                padding_top=20,  # Margen desde el borde superior
                children=[box]
            )
        )

    def _update_music_button_textures(self):
        """ Actualiza las texturas de los botones de música según el estado. """
        # Actualiza el botón de reproducir/pausar
        if self.music_player.is_playing:
            self.play_pause_button.texture = self.normal_texture_pause
            self.play_pause_button.texture_hovered = self.hover_texture_pause
            self.play_pause_button.texture_pressed = self.press_texture_pause
        else:
            self.play_pause_button.texture = self.normal_texture_play
            self.play_pause_button.texture_hovered = self.hover_texture_play
            self.play_pause_button.texture_pressed = self.press_texture_play

        # Actualiza el botón de silenciar
        if self.music_player.is_muted:
            self.mute_button.texture = self.normal_texture_mute_off
            self.mute_button.texture_hovered = self.hover_texture_mute_off
            self.mute_button.texture_pressed = self.press_texture_mute_off
        else:
            self.mute_button.texture = self.normal_texture_mute_on
            self.mute_button.texture_hovered = self.hover_texture_mute_on
            self.mute_button.texture_pressed = self.press_texture_mute_on

    def on_show_view(self):
        self.ui_manager.enable()


    def on_draw(self):
        self.clear()
        print("Tipo:", type(self.background_sprite))
        # ✅ Dibuja el fondo sin errores
        if self.background_sprite:
           self.background_sprite.draw()

        # ✅ Interfaz musical y texto
        self.ui_manager.draw()
        arcade.draw_text(
            f"Reproduciendo: {self.music_player.get_current_song_name()}",
            20,
            self.window.height - 30,
            arcade.color.WHITE,
            16
        )

    def on_resize(self, width, height):
        super().on_resize(width, height)
        print(f"Ventana redimensionada a {width}x{height}")
        self.background_sprite.center_x = width // 2
        self.background_sprite.center_y = height // 2

    def on_mouse_motion(self, x, y, dx, dy):
        """ Se llama cuando el ratón se mueve. """
        # Actualiza las coordenadas del ratón en la vista
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """ Se llama cuando se presiona un botón del ratón. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Botones del menú principal
            if self._check_button_click(x, y, self.window.width / 2, self.window.height / 2 + 50, 300, 70):
                self.window.show_view(self.window.game_view)
            elif self._check_button_click(x, y, self.window.width / 2, self.window.height / 2 - 40, 300, 70):
                arcade.exit()

    def _draw_button(self, text, center_x, center_y, width, height):
        """
        Función auxiliar para dibujar los botones principales del menú.
        """
        x1 = center_x - width / 2
        x2 = center_x + width / 2
        y1 = center_y - height / 2
        y2 = center_y + height / 2

        color_fondo = arcade.color.DARK_SLATE_GRAY
        # Simple hover effect for menu buttons (not using UIManager for these)
        # CORREGIDO: Usar self.mouse_x y self.mouse_y de la vista
        if x1 <= self.mouse_x <= x2 and y1 <= self.mouse_y <= y2:
            color_fondo = arcade.color.BLUE_SAPPHIRE

        arcade.draw_lrbt_rectangle_filled(x1, x2, y1, y2, color_fondo)

        arcade.Text(
            text, center_x, center_y, arcade.color.WHITE, 50,
            anchor_x="center", anchor_y="center"
        ).draw()

    def _check_button_click(self, x, y, center_x, center_y, width, height):
        """
        Función auxiliar para verificar clics en los botones principales del menú.
        """
        x1 = center_x - width / 2
        x2 = center_x + width / 2
        y1 = center_y - height / 2
        y2 = center_y + height / 2
        return x1 <= x <= x2 and y1 <= y <= y2




class MyGame(arcade.Window):
    """
    Ventana principal del juego.
    """
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Inicializa la instancia de MusicPlayer
        self.music_player = MusicPlayer()
        # Pasa la instancia de music_player a las vistas
        self.main_menu_view = MainMenuView(self, self.music_player)
        self.game_view = GameView(self, self.music_player)
        self.show_view(self.main_menu_view)

        # Inicia la reproducción de música cuando el juego se inicia, si hay canciones configuradas
        if self.music_player.song_list:
            self.music_player.play_pause() # Reproduce la primera canción al iniciar el menú

def main():
    """ Función principal para ejecutar el juego. """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
