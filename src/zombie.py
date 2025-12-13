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
            """Ссылка на игрока"""
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

    def __init__(self, x, y, zombie_type="normal", wave=1):
        self.center_x = x
        self.center_y = y
        self.radius = ZOMBIE_RADIUS
        self.type = zombie_type

        base_health = {"normal": 50, "fast": 30, "tank": 150, "toxic": 40}[zombie_type]
        base_speed = {"normal": 40, "fast": 80, "tank": 50, "toxic": 70}[zombie_type]
        damage = {"normal": 10, "fast": 12, "tank": 20, "toxic": 8}[zombie_type]
        points = {"normal": 10, "fast": 20, "tank": 30, "toxic": 25}[zombie_type]

        health = int(base_health * (1 + (wave - 1) * 0.2))

        self.stats = self.Stats(health=health, speed=base_speed, damage=damage, points=points)
        self.color = {
            "normal": COLOR_NORMAL,
            "fast": COLOR_FAST,
            "tank": COLOR_TANK,
            "toxic": COLOR_TOXIC
        }[zombie_type]

        """Временно, будет переназначен в WaveManager"""
        self.ai = self.AI(self, None)

    def update(self, delta_time):
        self.ai.update(delta_time)

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, self.color)
        """Отображение здоровья (полоса сверху)"""
        health_width = 30 * (self.stats.health / (self.stats.health / (self.stats.health > 0)))
        arcade.draw_rect_filled(arcade.rect.XYWH(self.center_x, self.center_y + self.radius + 5, health_width, 5),
                                arcade.color.RED)

    def take_damage(self, damage):
        self.stats.health -= damage
        return self.stats.health <= 0

    def on_death(self):
        if self.type == "toxic":
            pass
        return self.stats.points
