import arcade
import math
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Zombie(arcade.Sprite):
    def __init__(self, x, y, zombie_type="basic", wave=1):
        super().__init__()

        self.center_x = x
        self.center_y = y
        self.type = zombie_type

        frame_counts = {"basic": 16, "fast": 13, "fat": 8}
        frame_count = frame_counts.get(zombie_type, 4)
        self.textures = []
        for i in range(frame_count):
            path = f"assets/images/zombies/{zombie_type}/{zombie_type}_zombie_{i}.png"
            self.textures.append(arcade.load_texture(path))

        self.set_texture(0)
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        sizes = {
            "basic": (60 * 0.5, 89 * 0.5),
            "fast": (45 * 0.5, 75 * 0.5),
            "fat": (85 * 0.5, 170 * 0.5)
        }
        self.custom_width, self.custom_height = sizes.get(
            zombie_type, (60 * 0.5, 89 * 0.5))

        base_width = self.textures[0].width if self.textures else 60
        self.scale = self.custom_width / base_width

        base_health = {"basic": 50, "fast": 30, "fat": 150}
        base_speed = {"basic": 50, "fast": 100, "fat": 30}
        damage = {"basic": 10, "fast": 12, "fat": 20}
        points = {"basic": 10, "fast": 20, "fat": 30}

        health = int(base_health[zombie_type] * (1 + (wave - 1) * 0.2))
        self.max_health = health
        self.health = self.max_health
        self.speed = base_speed[zombie_type]
        self.damage = damage[zombie_type]
        self.points = points[zombie_type]

        self.player = None
        self._facing_right = True

    def update(self, delta_time):
        if self.player:
            dx = self.player.center_x - self.center_x
            dy = self.player.center_y - self.center_y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.center_x += (dx / dist) * self.speed * delta_time
                self.center_y += (dy / dist) * self.speed * delta_time

                self._facing_right = dx >= 0

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures)
            base_tex = self.textures[self.current_frame]
            if self._facing_right:
                self.texture = base_tex
            else:
                self.texture = base_tex.flip_horizontally()

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def on_death(self):
        return self.points

    def draw_health_bar(self):
        if self.health <= 0:
            return
        health_percent = self.health / self.max_health
        bar_width = 40
        current_width = bar_width * health_percent
        bar_x = self.center_x
        bar_y = self.center_y + self.custom_height / 2 + 10

        arcade.draw_rect_filled(
            arcade.XYWH(bar_x, bar_y, bar_width, 6),
            arcade.color.DARK_GRAY
        )
        health_color = arcade.color.RED
        if health_percent > 0.75:
            health_color = arcade.color.GREEN
        elif health_percent > 0.5:
            health_color = arcade.color.ORANGE

        arcade.draw_rect_filled(
            arcade.XYWH(bar_x, bar_y, current_width, 6),
            health_color
        )
        arcade.draw_rect_outline(
            arcade.XYWH(bar_x, bar_y, bar_width, 6),
            arcade.color.BLACK, 1
        )
