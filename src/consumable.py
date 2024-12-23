import pygame
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")

class Consumable:
    def __init__(self, name, effect, magnitude, duration,image, timer):
        self.name = name
        self.effect = effect  # e.g., "heal", "speed", "damage", "luck"
        self.magnitude = magnitude
        self.duration = duration  # Effect duration in seconds
        
        if isinstance(image, str):
            # It's a file path
            self.image = pygame.image.load(image).convert_alpha()
        else:
            # It's already a surface
            self.image = image
        self.game_timer = timer  # Store reference to the global Timer
        self.start_time = None   
        self.is_active = False  # Track whether the consumable is in use
        self.is_used = False


    def apply_effect(self, player):
        """Apply the effect to the player."""
        if not self.is_active:
            self.is_active = True
            self.is_used = True
            self.start_time = pygame.time.get_ticks() / 1000
            if self.effect == "heal":
                player.hp = min(player.hp + self.magnitude, player.max_hp)
                logging.info(f"{self.name} applied: Heal {self.magnitude}")
            elif self.effect in ["movement_speed", "damage", "luck"]:
                player.add_buff(self.effect, self.magnitude, self.duration)
                logging.info(f"{self.name} applied: {self.effect.capitalize()} +{self.magnitude} for {self.duration}s")
            
            
    
    def update(self):
        """Check if the consumable's duration has expired."""
        if self.is_active and self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() / 1000 - self.start_time
            if elapsed_time >= self.duration:
                self.is_active = False  # Mark consumable as inactive
    def get_time_remaining(self):
        """Return the remaining time for the effect."""
        if self.is_active and self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() / 1000 - self.start_time
            return max(0, self.duration - elapsed_time)
        return 0

class ConsumableManager:
    def __init__(self, json_file, game_timer):
        """
        :param json_file: Path to the JSON file with consumable definitions.
        :param game_timer: Reference to your global Timer instance.
        """
        self.game_timer = game_timer
        self.consumables = self.load_consumables(json_file)

    def load_consumables(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)

        # First pass: create Consumables that store surfaces, not just strings
        # i.e. "blueprints" that are themselves Consumables
        consumables = {}
        for name, props in data.items():
            path = props["image"]
            loaded_image = pygame.image.load(path).convert_alpha()

            blueprint = Consumable(
                name=name,
                effect=props["effect"],
                magnitude=props["magnitude"],
                duration=props["duration"],
                image=loaded_image,  # pass the surface directly
                timer=self.game_timer
            )
            consumables[name] = blueprint

        return consumables

    def create_consumable(self, name):
        # This retrieves the blueprint Consumable
        blueprint = self.consumables.get(name)
        if not blueprint:
            return None

        # Now create a new Consumable with same properties but a new fresh start_time, etc.
        return Consumable(
            name=blueprint.name,
            effect=blueprint.effect,
            magnitude=blueprint.magnitude,
            duration=blueprint.duration,
            image=blueprint.image,  # pass the loaded Surface
            timer=self.game_timer
        )
