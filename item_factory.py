# item_factory.py
import pygame
from src.item import Item

class ItemFactory:
    def __init__(self):
        self.item_data = self.load_item_data()

    def load_item_data(self):
        # Load item data from a configuration file or define it here
        item_data = {
            "health_potion": {
                "name": "Health Potion",
                "image": pygame.image.load("assets/images/items/Icon7.png").convert_alpha(),
                "effect": self.health_potion_effect
            },
            "damage_boost": {
                "name": "Damage Boost",
                "image": pygame.image.load("assets/images/items/Icon8.png").convert_alpha(),
                "effect": self.damage_boost_effect
            },
            "speed_boost": {
                "name": "Speed Boost",
                "image": pygame.image.load("assets/images/items/Icon9.png").convert_alpha(),
                "effect": self.speed_boost_effect
            },
            "attack_speed_boost": {
                "name": "AttackSpeed Boost",
                "image": pygame.image.load("assets/images/items/Icon9.png").convert_alpha(),
                "effect": self.attack_speed_boost_effect
            },
            "luck_boost": {
                "name": "Luck Boost",
                "image": pygame.image.load("assets/images/items/Icon9.png").convert_alpha(),
                "effect": self.luck_boost_effect
            },
            # Add more items as needed
        }
        return item_data

    def create_item(self, x, y, item_type):
        data = self.item_data[item_type]
        image = data["image"]
        effect = data["effect"]
        item = Item(x, y, item_type, image, effect)
        return item

    # Define item effects
    def health_potion_effect(self, player):
        player.hp = min(player.max_hp, player.hp + 10)  # Heal 50 HP

    def damage_boost_effect(self, player):
        player.damage += 10
        # Optionally, implement a timer to revert the effect after some time

    def speed_boost_effect(self, player):
        player.speed *= 1.05
    def attack_speed_boost_effect(self, player):
        player.fire_rate -= player.fire_rate * 0.15
        # Optionally, implement a timer to revert the effect after some time
    def luck_boost_effect(self, player):
        player.luck += 1
    # Add more effect methods as needed
