import pygame
from src.floating_text import FloatingText
from src.enemy import EnemyManager, load_enemy_data, spawn_enemy
from settings import *

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.tile_sprite = pygame.image.load("assets/images/backgrounds/grass_512x512.png").convert()
        self.objects = []
        self.dynamic_objects = []
        self.enemies = []
        self.astral_shards = []
        self.floating_texts = []
        self.generate_tiled_background()

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def generate_tiled_background(self):
        tile_width = self.tile_sprite.get_width()
        tile_height = self.tile_sprite.get_height()
        for y in range(0, self.height, tile_height):
            for x in range(0, self.width, tile_width):
                self.surface.blit(self.tile_sprite, (x, y))

    def add_floating_text(self, text, target, offset, color, duration=0.5, font=None):
        floating_text = FloatingText(text, target, offset, color, duration, font)
        self.floating_texts.append(floating_text)

    def check_shard_collection(self, player):
        for shard in self.astral_shards[:]:
            if shard.rect.colliderect(player.rect):
                player.collect_astral_shard()
                self.remove_astral_shard(shard)

    def add_astral_shard(self, astral_shard):
        self.astral_shards.append(astral_shard)
        self.add_object(astral_shard)

    def remove_astral_shard(self, astral_shard):
        if astral_shard in self.astral_shards:
            self.astral_shards.remove(astral_shard)
        self.remove_object(astral_shard)

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def draw(self, screen, camera):
        screen.blit(self.surface, (-camera.offset.x, -camera.offset.y))
        for obj in self.objects:
            obj.draw(screen, camera)
        for enemy in self.enemies:
            enemy.draw(screen, camera)
        for text in self.floating_texts:
            text.draw(screen, camera)

    def update(self):
        for obj in self.dynamic_objects:
            obj.update()
        for enemy in self.enemies:
            enemy.update()
        self.floating_texts = [text for text in self.floating_texts if not text.update()]

    def get_camera_offset(self, player_rect, screen_width, screen_height):
        offset_x = max(0, min(player_rect.centerx - screen_width // 2, self.width - screen_width))
        offset_y = max(0, min(player_rect.centery - screen_height // 2, self.height - screen_height))
        return offset_x, offset_y
