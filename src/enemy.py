import pygame
import json
import random
import math
from settings import *
from src.healthbar import HealthBar
from src.astral_shard import AstralShard
from src.weapon import Projectile

# -------------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------------

def load_enemy_data(json_file):
    """Load enemy definitions from a JSON file."""
    with open(json_file, "r") as f:
        return json.load(f)

def spawn_enemy(enemy_data, world_width, world_height, world):
    """Spawn a random enemy from the available enemy_data."""
    x, y = random.randint(0, world_width), random.randint(0, world_height)
    enemy_type = random.choice(list(enemy_data.keys()))
    properties = enemy_data[enemy_type]
    return Enemy(x, y, properties, world)

# -------------------------------------------------------------------------
# Base Enemy Class
# -------------------------------------------------------------------------

class Enemy:
    def __init__(self, x, y, properties, world):
        self.world = world
        self.position = pygame.math.Vector2(x, y)

        # Load and scale the enemy image
        self.size = properties.get("size", 1)
        self.image = pygame.image.load(properties["image"]).convert_alpha()
        original_w, original_h = self.image.get_width(), self.image.get_height()
        self.image = pygame.transform.scale(
            self.image,
            (int(original_w * self.size), int(original_h * self.size))
        )

        self.rect = self.image.get_rect(center=(x, y))

        # Enemy stats
        self.hp = self.max_hp = properties["hp"]
        self.damage = properties["damage"]
        self.speed = properties["movement_speed"]
        self.astral_shards_drop = properties["astral_shards_drop"]

        # Health bar
        self.health_bar = HealthBar(
            width=40, height=6,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            background_color=(128, 128, 128)
        )

    def move_towards_player(self, player_position):
        """
        Basic movement that slightly randomizes the angle 
        so enemies don't move in a perfect straight line.
        """
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

    def update(self, player_position, player):
        """
        Default update: move toward the player.
        (No timer needed for normal enemies.)
        """
        self.move_towards_player(player_position)

    def draw(self, screen, camera):
        """
        Draw the enemy and its health bar.
        """
        screen_position = camera.apply(self.rect)
        screen.blit(self.image, screen_position.topleft)

        health_bar_position = (screen_position.x, screen_position.y - 10)
        self.health_bar.draw(screen, health_bar_position, self.hp, self.max_hp)

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
        """Drop astral shards around the enemy's position."""
        for _ in range(self.astral_shards_drop):
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-20, 20)
            shard_x = max(0, min(self.position.x + offset_x, self.world.width))
            shard_y = max(0, min(self.position.y + offset_y, self.world.height))
            shard = AstralShard(shard_x, shard_y)
            self.world.add_astral_shard(shard)

# -------------------------------------------------------------------------
# Demon Subclass
# -------------------------------------------------------------------------

class Demon(Enemy):
    def __init__(self, x, y, properties, world):
        """
        A specialized enemy that periodically jumps (disappears) and 
        reappears near the player, firing projectiles immediately.
        """
        super().__init__(x, y, properties, world)

        # Firing-related properties
        self.fire_rate = properties.get("shoot_cooldown", 2)      # seconds
        self.projectile_speed = properties.get("projectile_speed", 7)
        self.range = properties.get("projectile_range", 300)
        self.damage = properties.get("damage", 50)
        self.projectiles_per_circle = properties.get("projectiles_per_circle", 12)

        # Track last time demon fired (in seconds)
        self.last_shot_time = 0.0
        self.projectiles = []

        # Jump-related timing
        self.jump_cooldown = 20        # Jump every 20 seconds
        self.rise_time = 0.2            # 1 second rising
        self.disappear_time = 2.0       # 2 seconds invisible
        # total time in air = self.rise_time + self.disappear_time

        # Jump states: "idle", "rising", "disappeared", "reappearing"
        self.jump_state = "idle"
        self.jump_start_time = 0.0

        # Where demon will appear after the jump
        self.reappear_position = None

        # Track when the last jump finished
        self.last_jump_finish_time = 0.0

        # Load/scale the projectile image
        original_image = pygame.image.load("assets/images/projectiles/Fireball1.png").convert_alpha()
        scale_factor = 10
        w, h = original_image.get_width(), original_image.get_height()
        self.projectile_image = pygame.transform.scale(original_image, (w * scale_factor, h * scale_factor))

    # -------------------------
    # Jump Logic
    # -------------------------
    def is_jumping(self):
        return self.jump_state != "idle"

    def start_jump(self, player_position, timer):
        """Begin the jump sequence."""
        self.jump_state = "rising"
        self.jump_start_time = timer.get_time()

        # Random offset so the demon doesn't appear exactly on top of the player
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)

        # Clamp position within world boundaries
        new_x = max(0, min(self.world.width,  player_position.x + offset_x))
        new_y = max(0, min(self.world.height, player_position.y + offset_y))
        self.reappear_position = pygame.math.Vector2(new_x, new_y)

    def update_jump(self, timer):
        """
        Manage the demon's jump states:
          - "rising": move visually upward for self.rise_time
          - "disappeared": remain invisible for self.disappear_time
          - "reappearing": instantly teleport + fire
        """
        elapsed = timer.get_time() - self.jump_start_time

        if self.jump_state == "rising":
            # Move up for self.rise_time seconds
            if elapsed < self.rise_time:
                self.position.y -= 2
                self.rect.center = self.position
            else:
                # Switch to invisible
                self.jump_state = "disappeared"
                self.jump_start_time = timer.get_time()  # reset for the next phase

        elif self.jump_state == "disappeared":
            if elapsed < self.disappear_time:
                # Stay invisible
                pass
            else:
                # Reappear near the player
                self.jump_state = "reappearing"
                self.position = self.reappear_position
                self.rect.center = self.position

                # Fire immediately
                self.fire_projectiles(timer)

        elif self.jump_state == "reappearing":
            # Jump done
            self.jump_state = "idle"
            self.last_jump_finish_time = timer.get_time()

    # -------------------------
    # Firing Logic
    # -------------------------
    def can_fire(self, timer):
        """
        Demon can fire if:
          - It's not jumping
          - Enough time has passed since the last shot
        """
        if self.is_jumping():
            return False

        current_time = timer.get_time()
        return (current_time - self.last_shot_time) >= self.fire_rate

    def fire_projectiles(self, timer):
        """Fire a circle of projectiles around the demon."""
        self.last_shot_time = timer.get_time()
        angle_step = 360 / self.projectiles_per_circle

        for i in range(self.projectiles_per_circle):
            angle = math.radians(i * angle_step)
            direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            direction = direction.normalize()

            projectile_target = self.position + direction * self.range
            projectile = Projectile(
                self.position,
                projectile_target,
                self.projectile_speed,
                self.damage,
                self.range,
                self.projectile_image
            )
            self.projectiles.append(projectile)

    # -------------------------
    # Update & Draw Overrides
    # -------------------------
    def update(self, player_position, player, timer):
        """
        Demon update requires passing in `timer` for time-based actions.
        """
        # Possibly start a jump if we're idle
        time_since_jump = timer.get_time() - self.last_jump_finish_time
        if self.jump_state == "idle" and time_since_jump >= self.jump_cooldown:
            self.start_jump(player_position, timer)

        # Handle jump states or normal movement/fire
        if self.is_jumping():
            self.update_jump(timer)
        else:
            # Normal movement from Enemy
            super().update(player_position, player)
            # Fire if cooldown allows
            if self.can_fire(timer):
                self.fire_projectiles(timer)

        # Update existing projectiles
        self.projectiles = [p for p in self.projectiles if p.update([player])]

    def draw(self, screen, camera):
        """
        Don't draw the demon if in 'disappeared' state. 
        Always draw projectiles.
        """
        if self.jump_state != "disappeared":
            super().draw(screen, camera)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)

# -------------------------------------------------------------------------
# EnemyManager
# -------------------------------------------------------------------------

class EnemyManager:
    def __init__(self, enemy_data, world_width, world_height, world):
        self.enemy_data = enemy_data
        self.world_width = world_width
        self.world_height = world_height
        self.enemies = []
        self.world = world

    def spawn_enemies(self, count):
        """Spawn a specified number of random enemies."""
        for _ in range(count):
            self.enemies.append(spawn_enemy(
                self.enemy_data,
                self.world_width,
                self.world_height,
                self.world
            ))

    def update(self, player, timer):
        """
        Update all enemies. If an enemy is a Demon, call its update with `timer`.
        Other enemies get a normal update without the timer parameter.
        """
        for enemy in self.enemies:
            if isinstance(enemy, Demon):
                enemy.update(player.position, player, timer)
            else:
                enemy.update(player.position, player)

            # Check collision with player
            if enemy.rect.colliderect(player.rect):
                player.take_damage(enemy.damage)

        # Remove dead enemies
        self.enemies = [enemy for enemy in self.enemies if enemy.hp > 0]

    def draw(self, screen, camera):
        """Draw all enemies in the list."""
        for enemy in self.enemies:
            enemy.draw(screen, camera)
