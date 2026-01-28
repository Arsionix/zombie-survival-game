import arcade
import json


def play_sound_with_volume(sound):
    try:
        with open("settings.json", "r") as f:
            volume = json.load(f).get("volume", 0.7)
    except:
        volume = 0.7
    arcade.play_sound(sound, volume=volume)
