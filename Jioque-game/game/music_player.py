# game/music_player.py
import arcade
import os
import pyglet.media.player as pyglet_player
from .config import MUSIC_LIST

class MusicPlayer:
    def __init__(self):
        self.song_list = MUSIC_LIST
        self.current_song_index = 0
        self.current_player = None
        self._is_playing = False
        self._is_muted = False
        self._volume = 0.5
        self._loaded_sounds = {}

        for path in self.song_list:
            try:
                if os.path.exists(path):
                    self._loaded_sounds[path] = arcade.load_sound(path)
                else:
                    print(f"ADVERTENCIA (MusicPlayer): Archivo de música no encontrado: {path}")
            except Exception as e:
                print(f"ERROR (MusicPlayer): No se pudo cargar el sonido '{path}': {e}")

        if not self.song_list:
            print("Música: No se configuraron canciones.")
        elif not self._loaded_sounds:
            print("Música: No se pudo cargar ninguna canción.")

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def is_muted(self):
        return self._is_muted

    def _stop_current_player(self):
        if self.current_player:
            try:
                self.current_player.pause()
                self.current_player.seek(0)
            except Exception as e:
                print(f"ERROR (MusicPlayer): No se pudo pausar/reiniciar el reproductor: {e}")
            finally:
                self.current_player = None

    def _play_current_song(self):
        if not self.song_list or not self._loaded_sounds:
            print("Música: No hay canciones cargadas.")
            return

        current_song_path = self.song_list[self.current_song_index]
        if current_song_path not in self._loaded_sounds:
            print(f"ADVERTENCIA (MusicPlayer): Canción no válida: {current_song_path}")
            self.next_song()
            return

        sound = self._loaded_sounds[current_song_path]
        self._stop_current_player()

        try:
            self.current_player = sound.play(volume=self._volume if not self._is_muted else 0)
            if not isinstance(self.current_player, pyglet_player.Player):
                print(f"ADVERTENCIA (MusicPlayer): Tipo inesperado: {type(self.current_player)}")
                self.current_player = None
                return
            self.current_player.push_handlers(on_eos=self._music_over)
            self._is_playing = True
            print(f"Música: Reproduciendo {os.path.basename(current_song_path)}")
        except Exception as e:
            print(f"ERROR (MusicPlayer): No se pudo reproducir '{current_song_path}': {e}")
            self._is_playing = False

    def play_pause(self):
        if not self.song_list or not self._loaded_sounds:
            print("Música: No hay canciones para reproducir.")
            return

        if self._is_playing:
            if self.current_player:
                try:
                    self.current_player.pause()
                except Exception as e:
                    print(f"ERROR (MusicPlayer): Error al pausar: {e}")
            self._is_playing = False
            print(f"Música: Pausada {self.get_current_song_name()}")
        else:
            if self.current_player and hasattr(self.current_player, 'is_paused') and self.current_player.is_paused:
                try:
                    self.current_player.play()
                except Exception as e:
                    print(f"ERROR (MusicPlayer): Error al reanudar: {e}")
            else:
                self._play_current_song()
            self._is_playing = True
            print(f"Música: Reanudando/Reproduciendo {self.get_current_song_name()}")

    def next_song(self):
        if not self.song_list:
            print("Música: Lista vacía.")
            return
        self._stop_current_player()
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self._play_current_song()

    def previous_song(self):
        if not self.song_list:
            print("Música: Lista vacía.")
            return
        self._stop_current_player()
        self.current_song_index = (self.current_song_index - 1 + len(self.song_list)) % len(self.song_list)
        self._play_current_song()

    def toggle_mute(self):
        self._is_muted = not self._is_muted
        if self.current_player:
            try:
                self.current_player.set_volume(0 if self._is_muted else self._volume)
            except Exception as e:
                print(f"ERROR (MusicPlayer): Error al ajustar volumen: {e}")
        print("Música: Silenciada." if self._is_muted else f"Música: Volumen restaurado a {self._volume:.1f}")

    def volume_down(self):
        self._volume = max(0.0, self._volume - 0.1)
        if self.current_player:
            try:
                self.current_player.set_volume(self._volume)
            except Exception as e:
                print(f"ERROR (MusicPlayer): Error al bajar volumen: {e}")
        print(f"Volumen: {self._volume:.1f}")

    def volume_up(self):
        self._volume = min(1.0, self._volume + 0.1)
        if self.current_player:
            try:
                self.current_player.set_volume(self._volume)
            except Exception as e:
                print(f"ERROR (MusicPlayer): Error al subir volumen: {e}")
        print(f"Volumen: {self._volume:.1f}")

    def get_current_song_name(self):
        if self.song_list and self.current_song_index < len(self.song_list):
            return os.path.basename(self.song_list[self.current_song_index])
        return "No hay canción"

    def _music_over(self):
        print(f"Música: '{self.get_current_song_name()}' ha terminado.")
        if self.current_player:
            try:
                self.current_player.pop_handlers()
            except Exception as e:
                print(f"ERROR (MusicPlayer): Error al quitar manejadores: {e}")
            finally:
                self.current_player = None
        self._is_playing = False
        self.next_song()
