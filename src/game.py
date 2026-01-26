import arcade
import random
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .player import Player
from .bullet import Bullet
from .wave_manager import WaveManager
from .ui import GameOverView, MenuView, SettingView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player_list.append(self.player)
        self.player_hit_cooldown = 0

        self.wave_manager = WaveManager(self.player)
        self.wave_manager.current_wave = 0
        self.wave_manager.start_next_wave()

        self.shoot_sound = arcade.load_sound(":resources:/sounds/laser1.wav")
        self.hit_sound = arcade.load_sound(":resources:/sounds/hit3.wav")

        self.keys_pressed = set()

    def on_show(self):
        pass

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            arcade.load_texture("assets/images/ui/game_background.jpg"),
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        if self.wave_manager:
            self.wave_manager.draw()

        self.player_list.draw()
        self.bullet_list.draw()

        self.player.draw_health_bar()

    def on_update(self, delta_time):
        self.player_list.update(delta_time, self.keys_pressed)
        self.bullet_list.update(delta_time)

        if self.wave_manager:
            self.wave_manager.update(delta_time)

        self.player_list.update_animation(delta_time)

        self.check_collisions()

        weapon = self.player.current_weapon
        if weapon.is_reloading:
            weapon.reload_cooldown -= delta_time
            if weapon.reload_cooldown <= 0:
                weapon.is_reloading = False
                weapon.current_ammo = weapon.magazine_size

        if weapon.cooldown > 0:
            weapon.cooldown -= delta_time

        if self.player_hit_cooldown > 0:
            self.player_hit_cooldown -= delta_time

        if self.wave_manager.wave_active:
            weapon.auto_reload_if_empty()

        if self.player.health <= 0:
            self.game_over()

    def check_collisions(self):
        for bullet in self.bullet_list[:]:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.wave_manager.zombies)
            if hit_list:
                bullet.remove_from_sprite_lists()
                arcade.play_sound(self.hit_sound, volume=0.3)
                for zombie in hit_list:
                    if zombie.take_damage(bullet.damage):
                        self.wave_manager.kill_zombie(zombie)

        if self.player_hit_cooldown <= 0:
            hit_list = arcade.check_for_collision_with_list(
                self.player, self.wave_manager.zombies)
            if hit_list:
                total_damage = sum(zombie.damage for zombie in hit_list)
                self.player.health -= total_damage
                self.player_hit_cooldown = 1.0
                self.wave_manager.wave_stats["total_damage"] = (
                    self.wave_manager.wave_stats.get(
                        "total_damage", 0) + total_damage
                )

    def game_over(self):
        game_over_view = GameOverView()

        game_over_view.final_score = self.wave_manager.upgrade_system.get_points()
        game_over_view.final_wave = self.wave_manager.current_wave

        self.window.show_view(game_over_view)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (hasattr(self, 'wave_manager') and self.wave_manager and
                hasattr(self.wave_manager, 'show_upgrade_menu') and
                    self.wave_manager.show_upgrade_menu):

                self.wave_manager.on_mouse_press(x, y, button)
            else:
                if not self.player.current_weapon.is_reloading:
                    self.player.current_weapon.shoot(
                        self.player, x, y, self.bullet_list)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if key == arcade.key.SPACE:
            if (hasattr(self, 'wave_manager') and self.wave_manager and
                hasattr(self.wave_manager, 'show_upgrade_menu') and
                    self.wave_manager.show_upgrade_menu):

                self.wave_manager.show_upgrade_menu = False
                self.wave_manager.wave_active = True
                self.wave_manager.show_player = True
                self.wave_manager.wave_timer = self.wave_manager.wave_start_delay
                return

        if key == arcade.key.R:
            if self.wave_manager.wave_active:
                self.player.current_weapon.start_reload()

        if key == arcade.key.ESCAPE:
            self.keys_pressed.clear()
            if hasattr(self.wave_manager, 'uimanager'):
                self.wave_manager.uimanager.disable()
            menu_view = MenuView()
            self.window.show_view(menu_view)
            return

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
