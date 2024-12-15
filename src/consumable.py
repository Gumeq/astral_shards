import pygame
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")

class Consumable:
    def __init__(self, name, effect, magnitude, duration,image):
        self.name = name
        self.effect = effect  # e.g., "heal", "speed", "damage", "luck"
        self.magnitude = magnitude
        self.duration = duration  # Effect duration in seconds
        self.image = pygame.image.load(image).convert_alpha()
        self.start_time = None  # Time when the effect starts
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
    def __init__(self, json_file):
        self.consumables = self.load_consumables(json_file)

    def load_consumables(self, json_file):
        """Load consumables from a JSON file."""
        with open(json_file, "r") as f:
            data = json.load(f)
        return {name: Consumable(**props) for name, props in data.items()}

    def create_consumable(self, name):
        """Create a consumable instance by name."""
        return self.consumables.get(name)
