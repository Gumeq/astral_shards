import pygame
from src.item import Item
import json

class ItemFactory:
    def __init__(self, config_path="assets/config/items.json", scale_factor=2):
        # Initialize effect handlers before loading item data
        self.effect_handlers = {
            "health_potion": self.health_potion_effect,
            "damage_boost": self.damage_boost_effect,
            "speed_boost": self.speed_boost_effect,
            "attack_speed_boost": self.attack_speed_boost_effect,
            "luck_boost": self.luck_boost_effect,
        }
        self.scale_factor = scale_factor  # Scaling factor for item images
        self.item_data = self.load_item_data(config_path)

    def load_item_data(self, config_path):
        """Load item data from a JSON file."""
        try:
            with open(config_path, "r") as file:
                item_data = json.load(file)
        except FileNotFoundError:
            raise RuntimeError(f"Item configuration file not found: {config_path}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON format in item configuration file: {config_path}")

        # Preload images, scale them, and assign effects dynamically
        for key, data in item_data.items():
            try:
                image = pygame.image.load(data["image_path"]).convert_alpha()
                # Scale the image
                scaled_image = pygame.transform.scale(
                    image,
                    (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor))
                )
                data["image"] = scaled_image
                data["effect"] = self.effect_handlers.get(key, self.default_effect)
            except pygame.error as e:
                raise RuntimeError(f"Error loading image for item '{key}': {e}")
        return item_data

    def create_item(self, x, y, item_type):
        """Create an item based on its type."""
        if item_type not in self.item_data:
            raise ValueError(f"Unknown item type: {item_type}")
        data = self.item_data[item_type]
        return Item(x, y, item_type, data["image"], data["effect"])

    # Define item effects
    def health_potion_effect(self, player):
        player.hp = min(player.max_hp, player.hp + 10)  # Heal 10 HP

    def damage_boost_effect(self, player):
        player.damage += 10

    def speed_boost_effect(self, player):
        player.speed *= 1.05

    def attack_speed_boost_effect(self, player):
        player.fire_rate -= player.fire_rate * 0.15

    def luck_boost_effect(self, player):
        player.luck += 1

    def default_effect(self, player):
        """Fallback effect if no handler is found."""
        print("No effect applied for this item.")
