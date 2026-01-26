import arcade
import math


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, player, speed=800, base_damage=25, texture_path=None):
        super().__init__(texture_path, scale=0.2)

        self.center_x = start_x
        self.center_y = start_y

        dx = target_x - start_x
        dy = target_y - start_y
        angle = math.atan2(dy, dx)
        self.angle = math.degrees(angle) + 90

        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        self.damage = base_damage * player.damage_multiplier

        self.max_distance = 1000
        self.distance_traveled = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.distance_traveled += math.hypot(
            self.change_x * delta_time, self.change_y * delta_time)

        if self.distance_traveled > self.max_distance:
            self.remove_from_sprite_lists()
