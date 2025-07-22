import arcade
import os
import time

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 0.5
        self.center_x = 400
        self.center_y = 300
        self.change_x = 0

        # Física
        self.velocity_y = 0
        self.gravity = -0.5
        self.on_ground = True
        self.ground_y = 300

        # Animación
        self.textures = []
        self.cur_frame = 0
        self.frame_timer = 0.0
        self.frame_interval = 0.15
        self.animation_name = "idle"
        self.jump_frame_countdown = 0

        self.frame_count = {
            "idle": 4,
            "jumps": 14,
            "jump": 20
        }
        self.animation_paths = {
            "idle": "assets/images/player/idle_frames/",
            "jumps": "assets/images/player/jumps_frames/",
            "jump": "assets/images/player/jump_frames/"
        }
        self.animation_scales = {
            "idle": 1.0,
            "jumps": 0.5,
            "jump": 0.5
        }

        # Salto por doble pulsación
        self.up_press_times = []
        self.double_press_window = 0.4

        self.load_animation("idle")

    def load_animation(self, name: str):
        self.textures = []
        folder = self.animation_paths.get(name, "")
        total = self.frame_count.get(name, 1)
        scale = self.animation_scales.get(name, 1.0)

        for i in range(total):
            path = os.path.join(folder, f"{i}.png")
            if os.path.exists(path):
                self.textures.append(arcade.load_texture(path))
            else:
                print(f"⚠️ Frame no encontrado: {path}")

        if self.textures:
            self.texture = self.textures[0]
            self.animation_name = name
            self.cur_frame = 0
            self.frame_timer = 0.0
            self.scale = scale
            self.frame_interval = 0.08 if name != "idle" else 0.15
            self.jump_frame_countdown = len(self.textures)
        else:
            self.textures = [arcade.make_circle_texture(64, arcade.color.RED)]
            self.texture = self.textures[0]
            self.animation_name = "fallback"

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x

        # Física vertical
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.center_y += self.velocity_y

            if self.center_y <= self.ground_y:
                self.center_y = self.ground_y
                self.velocity_y = 0
                self.on_ground = True

        # Animación por frame
        if len(self.textures) > 1:
            self.frame_timer += delta_time
            if self.frame_timer >= self.frame_interval:
                self.cur_frame = (self.cur_frame + 1) % len(self.textures)
                self.texture = self.textures[self.cur_frame]
                self.frame_timer -= self.frame_interval

                if self.animation_name in ("jump", "jumps"):
                    self.jump_frame_countdown -= 1
                    if self.jump_frame_countdown <= 0:
                        self.load_animation("idle")

    def register_up_press(self):
        now = time.time()
        self.up_press_times = [t for t in self.up_press_times if now - t <= self.double_press_window]
        self.up_press_times.append(now)

        if len(self.up_press_times) == 2:
            # Salto largo
            if self.animation_name == "jumps":
                self.velocity_y = 12
                self.load_animation("jump")
            elif self.on_ground:
                self.velocity_y = 12
                self.on_ground = False
                self.load_animation("jump")
            self.up_press_times.clear()

        elif len(self.up_press_times) == 1 and self.on_ground:
            # Salto corto
            self.velocity_y = 8
            self.on_ground = False
            self.load_animation("jumps")
