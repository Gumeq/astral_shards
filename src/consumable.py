import pygame
import json
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")

class Consumable:
    def __init__(self, name, effect, magnitude, duration, image, timer):
        self.name = name
        self.effect = effect
        self.magnitude = magnitude
        self.duration = duration
        self.image = pygame.image.load(image).convert_alpha() if isinstance(image, str) else image
        self.game_timer = timer
        self.start_time = None
        self.is_active = False
        self.is_used = False

    def apply_effect(self, player):
        if not self.is_active:
            self.is_active = True
            self.is_used = True
            self.start_time = pygame.time.get_ticks() / 1000
            if self.effect == "heal":
                player.hp = min(player.hp + self.magnitude, player.max_hp)
                logging.info(f"{self.name} applied: Heal {self.magnitude}")
            elif self.effect in ["movement_speed", "damage", "luck", "ability_power"]:
                player.add_buff(self.effect, self.magnitude, self.duration)
                logging.info(f"{self.name} applied: {self.effect.capitalize()} +{self.magnitude} for {self.duration}s")

    def update(self):
        if self.is_active and self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() / 1000 - self.start_time
            if elapsed_time >= self.duration:
                self.is_active = False

    def get_time_remaining(self):
        if self.is_active and self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() / 1000 - self.start_time
            return max(0, self.duration - elapsed_time)
        return 0

class ConsumableManager:
    def __init__(self, json_file, game_timer):
        self.game_timer = game_timer
        self.consumables = self.load_consumables(json_file)

    def load_consumables(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        consumables = {}
        for name, props in data.items():
            loaded_image = pygame.image.load(props["image"]).convert_alpha()
            consumables[name] = Consumable(
                name=name,
                effect=props["effect"],
                magnitude=props["magnitude"],
                duration=props["duration"],
                image=loaded_image,
                timer=self.game_timer
            )
        return consumables

    def create_consumable(self, name):
        blueprint = self.consumables.get(name)
        if not blueprint:
            return None
        return Consumable(
            name=blueprint.name,
            effect=blueprint.effect,
            magnitude=blueprint.magnitude,
            duration=blueprint.duration,
            image=blueprint.image,
            timer=self.game_timer
        )
