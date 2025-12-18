"""
Класс зомби, с их спавном с помощью AI и их характеристиками
"""

import arcade
import math

ZOMBIE_RADIUS = 15
COLOR_NORMAL = arcade.color.DARK_GREEN
COLOR_FAST = arcade.color.YELLOW
COLOR_TANK = arcade.color.DARK_GRAY
COLOR_TOXIC = arcade.color.LIME_GREEN


class Zombie:
    class Stats:
        def __init__(self, health, speed, damage, points):
            self.health = health
            self.speed = speed
            self.damage = damage
            self.points = points

    class AI:
        def __init__(self, zombie, player):
            self.zombie = zombie
            self.player = player

        def update(self, delta_time):
            dx = self.player.center_x - self.zombie.center_x
            dy = self.player.center_y - self.zombie.center_y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.zombie.center_x += dx * self.zombie.stats.speed * delta_time
                self.zombie.center_y += dy * self.zombie.stats.speed * delta_time

    SPRITE_INFO = {
        "normal": {"file": "basic_zombie.png", "rows": 1, "cols": 16, "width": 2000 // 16, "height": 140, "scale": 0.7},
        "fast": {"file": "fast_zombie.png", "rows": 1, "cols": 13, "width": 780 // 13, "height": 75, "scale": 1.0},
        "tank": {"file": "fat_zombie.png", "rows": 1, "cols": 8, "width": 1280 // 8, "height": 170, "scale": 0.8},
        "toxic": {"file": "poison_zombie.png", "rows": 1, "cols": 8, "width": 1080 // 8, "height": 126, "scale": 0.7},
    }

    def __init__(self, x, y, zombie_type="normal", wave=1):
        self.center_x = x
        self.center_y = y
        self.type = zombie_type
        self.scale = self.SPRITE_INFO[zombie_type]["scale"]
        self.health_bar_width = 40

        info = self.SPRITE_INFO[zombie_type]
        self.sprite_sheet = arcade.load_texture(info["file"])
        self.frames = []
        for col in range(info["cols"]):
            frame = arcade.Texture(
                name=f"{zombie_type}_frame_{col}",
                image=arcade.load_texture(info["file"]).image.crop((
                    col * info["width"],
                    0,
                    (col + 1) * info["width"],
                    info["height"]
                ))
            )
            self.frames.append(frame)

        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.1

        base_health = {"normal": 50, "fast": 30, "tank": 150, "toxic": 40}[zombie_type]
        base_speed = {"normal": 50, "fast": 100, "tank": 30, "toxic": 70}[zombie_type]
        damage = {"normal": 10, "fast": 12, "tank": 20, "toxic": 8}[zombie_type]
        points = {"normal": 10, "fast": 20, "tank": 30, "toxic": 25}[zombie_type]

        health = int(base_health * (1 + (wave - 1) * 0.2))
        self.stats = self.Stats(health=health, speed=base_speed, damage=damage, points=points)

        self.ai = self.AI(self, None)
        self.width = info["width"] * self.scale
        self.height = info["height"] * self.scale

    def update(self, delta_time):
        self.ai.update(delta_time)

        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_time = 0

    def draw(self):
        dx = self.ai.player.center_x - self.center_x
        scale_x = self.width  # Если положительная ширина, то зомби смотрит вправо
        if dx < 0:  # Если игрок слева, то зомби смотрит влево
            scale_x = -self.width

        texture = self.frames[self.current_frame]
        arcade.draw_texture_rect(
            texture,
            arcade.XYWH(
                self.center_x,
                self.center_y,
                scale_x,
                self.height
            )
        )

        # Здоровье
        health_width = self.health_bar_width * (self.stats.health / max(self.stats.health, 1))
        arcade.draw_rect_filled(
            arcade.XYWH(self.center_x, self.center_y + self.height / 2 + 10, health_width, 6),
            arcade.color.RED
        )
        arcade.draw_rect_outline(
            arcade.XYWH(self.center_x, self.center_y + self.height / 2 + 10, self.health_bar_width, 6),
            arcade.color.BLACK, border_width=1
        )

    def take_damage(self, damage):
        self.stats.health -= damage
        return self.stats.health <= 0

    def on_death(self):
        pass
