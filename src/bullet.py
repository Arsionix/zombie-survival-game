import arcade
import math
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Bullet(arcade.Sprite):

    def __init__(self, start_x, start_y, target_x, target_y, player, speed=800, base_damage=10):
        """
        Инициализирует пулю с заданными параметрами.

        Параметры:
            start_x: Начальная координата X
            start_y: Начальная координата Y
            target_x: Целевая координата X (курсор мыши)
            target_y: Целевая координата Y (курсор мыши)
            player: Объект игрока для расчета урона
            speed: Скорость пули
            base_damage: Базовый урон пули
        """
        super().__init__()
        self.texture = arcade.load_texture(
            ":resources:/images/space_shooter/laserBlue01.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed

        self.damage = base_damage * player.damage_multiplier

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.angle = math.degrees(-angle)

    def update(self, delta_time):
        """
        Обновляет позицию пули и удаляет ее при выходе за границы экрана.

        Параметры:
            delta_time: Время, прошедшее с предыдущего обновления
        """
        if (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
                self.center_y < 0 or self.center_y > SCREEN_HEIGHT):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
