import arcade
import math
from .bullet import Bullet


class Weapon:
    def __init__(self, weapon_type="pistol"):
        self.type = weapon_type
        self._load_config()
        self.current_ammo = self.magazine_size
        self.is_reloading = False
        self.reload_cooldown = 0.0

    def _load_config(self):
        configs = {
            "pistol": {
                "fire_rate": 2.0,
                "projectiles": 1,
                "spread": 0.0,
                "base_damage": 25,
                "name": "Пистолет",
                "bullet_texture": "assets/images/weapons/bullet_pistol.png",
                "sound": "assets/sounds/shoot/pistol_shot.wav",
                "reload_duration": 0.8,
                "reload_sound": "assets/sounds/shoot/reload_pistol.wav",
                "magazine_size": 8
            },
            "shotgun": {
                "fire_rate": 0.8,
                "projectiles": 2,
                "spread": 10.0,
                "base_damage": 14,
                "name": "Дробовик",
                "bullet_texture": "assets/images/weapons/bullet_shotgun.png",
                "sound": "assets/sounds/shoot/shotgun_shot.wav",
                "reload_duration": 1.5,
                "reload_sound": "assets/sounds/shoot/reload_shotgun.wav",
                "magazine_size": 6
            },
            "smg": {
                "fire_rate": 7.0,
                "projectiles": 1,
                "spread": 8.0,
                "base_damage": 12,
                "name": "Автомат",
                "bullet_texture": "assets/images/weapons/bullet_smg.png",
                "sound": "assets/sounds/shoot/smg_shot.wav",
                "reload_duration": 3.5,
                "reload_sound": "assets/sounds/shoot/reload_smg.wav",
                "magazine_size": 30
            },
            "sniper": {
                "fire_rate": 0.5,
                "projectiles": 1,
                "spread": 0.0,
                "base_damage": 120,
                "name": "Снайперка",
                "bullet_texture": "assets/images/weapons/bullet_sniper.png",
                "sound": "assets/sounds/shoot/sniper_shot.wav",
                "reload_duration": 2.5,
                "reload_sound": "assets/sounds/shoot/reload_sniper.wav",
                "magazine_size": 5
            }
        }

        cfg = configs.get(self.type, configs["pistol"])
        self.fire_rate = cfg["fire_rate"]
        self.projectiles = cfg["projectiles"]
        self.spread = cfg["spread"]
        self.base_damage = cfg["base_damage"]
        self.name = cfg["name"]
        self.bullet_texture = cfg["bullet_texture"]
        self.sound = arcade.load_sound(cfg["sound"])
        self.reload_duration = cfg["reload_duration"]
        self.magazine_size = cfg["magazine_size"]
        self.reload_sound = arcade.load_sound(cfg["reload_sound"])
        self.cooldown = 0.0

    def can_shoot(self):
        return self.cooldown <= 0

    def start_reload(self):
        if not self.is_reloading and self.current_ammo < self.magazine_size:
            self.is_reloading = True
            self.reload_cooldown = self.reload_duration
            arcade.play_sound(self.reload_sound)

    def auto_reload_if_empty(self):
        if self.current_ammo <= 0 and not self.is_reloading:
            self.start_reload()

    def shoot(self, player, target_x, target_y, bullet_list):
        if not self.can_shoot():
            return False
        if self.is_reloading or self.current_ammo <= 0:
            return False

        if self.current_ammo < self.projectiles:
            actual_projectiles = self.current_ammo
        else:
            actual_projectiles = self.projectiles

        self.current_ammo -= actual_projectiles

        dx = target_x - player.center_x
        dy = target_y - player.center_y
        base_angle = math.atan2(dy, dx)

        self.cooldown = 1.0 / self.fire_rate

        for i in range(actual_projectiles):
            if actual_projectiles == 1:
                angle = base_angle
            else:
                spread_rad = math.radians(self.spread)
                step = (2 * spread_rad) / (actual_projectiles - 1)
                offset = -spread_rad + i * step
                angle = base_angle + offset

            bullet = Bullet(
                start_x=player.center_x,
                start_y=player.center_y,
                target_x=player.center_x + math.cos(angle) * 1000,
                target_y=player.center_y + math.sin(angle) * 1000,
                player=player,
                speed=800,
                base_damage=self.base_damage,
                texture_path=self.bullet_texture
            )
            bullet_list.append(bullet)

        arcade.play_sound(self.sound)
        return True
