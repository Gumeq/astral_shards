import pygame
from settings import *
import json
import random
from src.healthbar import HealthBar
from src.astral_shard import AstralShard
import math

def load_enemy_data(json_file):
    """Load enemy properties from a JSON file."""
    with open(json_file, "r") as f:
        return json.load(f)

def spawn_enemy(enemy_data, world_width, world_height ,world):
    """Spawn an enemy at a random position within the world."""
    x = random.randint(0, world_width)
    y = random.randint(0, world_height)
    enemy_type = random.choice(list(enemy_data.keys()))
    properties = enemy_data[enemy_type]
    return Enemy(x, y, properties, world)

class Enemy:
    def __init__(self, x, y, properties, world):
        self.world = world
        self.position = pygame.math.Vector2(x, y)
        self.size = properties.get("size", 1)  # Default size is 1 (no scaling)
        self.image = pygame.image.load(properties["image"]).convert_alpha()
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image,
            (int(original_width * self.size), int(original_height * self.size))
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = properties["hp"]
        self.max_hp = properties["hp"]
        self.damage = properties["damage"]
        self.speed = properties["movement_speed"]
        self.astral_shards_drop = properties["astral_shards_drop"]
        self.health_bar = HealthBar(
            width=40,  # Fixed width
            height=6,  # Height of the health bar
            border_color=(255, 255, 255),  # White border
            fill_color=(255, 0, 0),  # Red fill
            background_color=(128, 128, 128)  # Gray background
        )

    def move_towards_player(self, player_position):
        """Move towards the player's position with a bit of randomness."""
        direction = player_position - self.position
        if direction.length() > 0:
            direction = direction.normalize()

            # Add a small random angle to the direction
            angle_variation = random.uniform(-5, 5)  # degrees
            angle_radians = math.radians(angle_variation)

            # Rotate the direction vector by angle_radians
            cos_a = math.cos(angle_radians)
            sin_a = math.sin(angle_radians)
            # Rotate the direction vector (x,y) around (0,0)
            rotated_x = direction.x * cos_a - direction.y * sin_a
            rotated_y = direction.x * sin_a + direction.y * cos_a
            direction = pygame.math.Vector2(rotated_x, rotated_y).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

    def draw(self, screen, camera):
        """Draw the enemy and their health bar."""
        screen_position = camera.apply(self.rect)
        screen.blit(self.image, screen_position.topleft)

        # Draw health bar above the enemy
        health_bar_position = (screen_position.x, screen_position.y - 10)
        self.health_bar.draw(screen, health_bar_position, self.hp, self.max_hp)


    def update(self, player_position):
        """Update the enemy's behavior."""
        self.move_towards_player(player_position)

    def take_damage(self, damage):
        """Reduce the enemy's health."""
        self.hp -= damage
        self.world.add_floating_text(
            text=str(damage),
            target = self,
            offset=(0, -20),  # Slightly above the player
            color=(255, 0, 0),  # Red for damage
        )
        if self.hp <= 0:
            self.die()

    def die(self):
        """Handle enemy death."""
        print(f"Enemy at {self.position} has died.")
        self.drop_astral_shard()
        
    def drop_astral_shard(self):
        """Drop astral shards at random nearby positions."""
        for _ in range(self.astral_shards_drop):
            # Add a small random offset to the shard's position
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)
            shard_x = self.position.x + offset_x
            shard_y = self.position.y + offset_y

            # Ensure the shard stays within the world bounds
            shard_x = max(0, min(shard_x, self.world.width))
            shard_y = max(0, min(shard_y, self.world.height))

            # Create and add the shard to the world
            shard = AstralShard(shard_x, shard_y)
            self.world.add_astral_shard(shard)
        
class EnemyManager:
    def __init__(self, enemy_data, world_width, world_height, world):
        self.enemy_data = enemy_data
        self.world_width = world_width
        self.world_height = world_height
        self.enemies = []
        self.world = world

    def spawn_enemies(self, count ):
        """Spawn multiple enemies."""
        for _ in range(count):
            enemy = spawn_enemy(self.enemy_data, self.world_width, self.world_height, self.world)
            self.enemies.append(enemy)

    def update(self, player):
        """Update all enemies and handle player collisions."""
        for enemy in self.enemies:
            enemy.update(player.position)
            # Check collision with player
            if enemy.rect.colliderect(player.rect):
                player.take_damage(enemy.damage)
                
        self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

    def draw(self, screen, camera):
        """Draw all enemies."""
        for enemy in self.enemies:
            enemy.draw(screen, camera)