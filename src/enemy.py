import pygame
import json
import random
import math
from settings import *
from src.healthbar import HealthBar
from src.astral_shard import AstralShard

def load_enemy_data(json_file):
    with open(json_file, "r") as f:
        return json.load(f)

def spawn_enemy(enemy_data, world_width, world_height, world):
    x, y = random.randint(0, world_width), random.randint(0, world_height)
    enemy_type = random.choice(list(enemy_data.keys()))
    properties = enemy_data[enemy_type]
    return Enemy(x, y, properties, world)

class Enemy:
    def __init__(self, x, y, properties, world):
        self.world = world
        self.position = pygame.math.Vector2(x, y)
        self.size = properties.get("size", 1)
        self.image = pygame.image.load(properties["image"]).convert_alpha()
        original_width, original_height = self.image.get_width(), self.image.get_height()
        self.image = pygame.transform.scale(
            self.image,
            (int(original_width * self.size), int(original_height * self.size))
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = self.max_hp = properties["hp"]
        self.damage = properties["damage"]
        self.speed = properties["movement_speed"]
        self.astral_shards_drop = properties["astral_shards_drop"]
        self.health_bar = HealthBar(40, 6, (255, 255, 255), (255, 0, 0), (128, 128, 128))

    def move_towards_player(self, player_position):
        direction = player_position - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            angle_variation = random.uniform(-5, 5)
            angle_radians = math.radians(angle_variation)
            cos_a, sin_a = math.cos(angle_radians), math.sin(angle_radians)
            rotated_x = direction.x * cos_a - direction.y * sin_a
            rotated_y = direction.x * sin_a + direction.y * cos_a
            self.position += pygame.math.Vector2(rotated_x, rotated_y).normalize() * self.speed
            self.rect.center = self.position

    def draw(self, screen, camera):
        screen_position = camera.apply(self.rect)
        screen.blit(self.image, screen_position.topleft)
        health_bar_position = (screen_position.x, screen_position.y - 10)
        self.health_bar.draw(screen, health_bar_position, self.hp, self.max_hp)

    def update(self, player_position):
        self.move_towards_player(player_position)

    def take_damage(self, damage):
        self.hp -= damage
        self.world.add_floating_text(
            text=str(damage),
            target=self,
            offset=(0, -20),
            color=(255, 0, 0)
        )
        if self.hp <= 0:
            self.die()

    def die(self):
        self.drop_astral_shard()

    def drop_astral_shard(self):
        for _ in range(self.astral_shards_drop):
            offset_x, offset_y = random.randint(-20, 20), random.randint(-20, 20)
            shard_x = max(0, min(self.position.x + offset_x, self.world.width))
            shard_y = max(0, min(self.position.y + offset_y, self.world.height))
            shard = AstralShard(shard_x, shard_y)
            self.world.add_astral_shard(shard)

class EnemyManager:
    def __init__(self, enemy_data, world_width, world_height, world):
        self.enemy_data = enemy_data
        self.world_width = world_width
        self.world_height = world_height
        self.enemies = []
        self.world = world

    def spawn_enemies(self, count):
        for _ in range(count):
            self.enemies.append(spawn_enemy(self.enemy_data, self.world_width, self.world_height, self.world))

    def update(self, player):
        for enemy in self.enemies:
            enemy.update(player.position)
            if enemy.rect.colliderect(player.rect):
                player.take_damage(enemy.damage)
        self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

    def draw(self, screen, camera):
        for enemy in self.enemies:
            enemy.draw(screen, camera)
