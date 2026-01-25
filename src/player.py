import arcade
import math
import enum
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.speed = 200
        self.max_health = 100
        self.health = self.max_health
        self.health_bar_width = 50

        self.damage_multiplier = 1.0
        self.fire_rate = 2.0
        self.shoot_cooldown = 0.0

        self.idle_texture = arcade.load_texture(
            "assets/images/player/player_idle.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(0, 8):
            texture = arcade.load_texture(
                f"assets/images/player/player_walk{i}.png")
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1

        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

    def draw_health_bar(self):
        if self.health > 0:
            health_percent = self.health / self.max_health
            current_width = self.health_bar_width * health_percent

            bar_x = self.center_x
            bar_y = self.center_y - self.height / 2 - 10

            arcade.draw_rect_filled(
                arcade.XYWH(bar_x, bar_y, self.health_bar_width, 6),
                arcade.color.DARK_GRAY
            )

            health_color = arcade.color.RED
            if health_percent > 0.5:
                health_color = arcade.color.ORANGE
            if health_percent > 0.75:
                health_color = arcade.color.GREEN

            arcade.draw_rect_filled(
                arcade.XYWH(bar_x, bar_y, current_width, 6),
                health_color
            )

            arcade.draw_rect_outline(
                arcade.XYWH(bar_x, bar_y, self.health_bar_width, 6),
                arcade.color.BLACK, 1
            )

    def update_animation(self, delta_time: float = 1/60):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally(
                    )

        else:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update(self, delta_time, keys_pressed):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= delta_time

        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy

        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.center_x = max(
            self.width/2, min(SCREEN_WIDTH - self.width/2, self.center_x))
        self.center_y = max(
            self.height/2, min(SCREEN_HEIGHT - self.height/2, self.center_y))

        self.is_walking = dx or dy
