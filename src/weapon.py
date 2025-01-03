import pygame
import json
import random
import math
from src.player import Player

class Weapon:
    def __init__(self, properties, player):
        self.player = player
        self.name = properties["name"]
        self.damage = properties["damage"]
        self.fire_rate = properties["fire_rate"]
        self.projectile_speed = properties["projectile_speed"]
        self.range = properties["range"]
        self.image = pygame.image.load(properties["image"]).convert_alpha()
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        self.image = pygame.transform.scale(
            self.image,
            (int(original_width * properties["scale"]), int(original_height * properties["scale"]))
        )
        self.cooldown = 1 / self.fire_rate
        self.last_shot_time = 0

    def can_fire(self):
        current_time = pygame.time.get_ticks() / 1000
        effective_fire_rate = self.fire_rate * self.player.attack_speed
        cooldown = 1 / effective_fire_rate
        return current_time - self.last_shot_time >= cooldown

    def fire(self, position, target_position, projectiles):
        if self.can_fire():
            self.last_shot_time = pygame.time.get_ticks() / 1000
            projectile = Projectile(
                position, target_position, self.projectile_speed + self.player.movement_speed ,
                self.damage * self.player.ability_power,
                self.range * self.player.attack_range,
                self.image
            )
            projectiles.append(projectile)

class Projectile:
    def __init__(self, position, target_position, speed, damage, range, image):
        self.position = pygame.math.Vector2(position)
        self.start_position = pygame.math.Vector2(position)
        self.target_position = pygame.math.Vector2(target_position)
        self.direction = (self.target_position - self.position).normalize()
        self.speed = speed
        self.damage = damage
        self.range = range
        self.original_image = image
        self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, targets):
        self.position += self.direction * self.speed
        self.rect.center = self.position
        if self.position.distance_to(self.start_position) > self.range:
            return False
        for target in targets:
            if self.rect.colliderect(target.rect):
                target.take_damage(self.damage)
                return False
        return True

    def draw(self, screen, camera):
        screen_position = camera.apply(self.rect)
        screen.blit(self.image, screen_position.topleft)

class WeaponManager:
    def __init__(self, weapon_data_file, player, projectiles):
        self.weapon_data = self.load_weapon_data(weapon_data_file)
        self.active_weapon = None
        self.projectiles = projectiles
        self.player = player

    def load_weapon_data(self, json_file):
        with open(json_file, "r") as f:
            return json.load(f)

    def equip_weapon(self, weapon_name):
        if weapon_name in self.weapon_data:
            self.active_weapon = Weapon(self.weapon_data[weapon_name], self.player)
        else:
            raise ValueError(f"Weapon '{weapon_name}' not found in weapon data.")

    def update(self, enemies):
        self.projectiles = [p for p in self.projectiles if p.update(enemies)]

    def draw(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)

    def fire_weapon(self, position, target_position):
        if self.active_weapon:
            self.active_weapon.fire(position, target_position, self.projectiles)
