import pygame
from settings import *
from src.healthbar import HealthBar
from src.inventory import Inventory
import random

class AnimationController:
    def __init__(self, animations, animation_speed=10):
        self.animations = animations
        self.current_animation = "Idle"
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()

    def set_animation(self, animation_name):
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

    def get_current_frame(self, facing_right=True):
        frame = self.animations[self.current_animation][self.current_frame]
        return pygame.transform.flip(frame, True, False) if not facing_right else frame

class Player:
    def __init__(self, x, y, animations, world, state_manager):
        self.world = world
        self.state_manager = state_manager
        self.position = pygame.math.Vector2(x, y)
        
        # Stats
        self.movement_speed = 5
        self.ability_power = 20
        self.hp = self.max_hp = 100
        self.luck = 1
        self.astral_shards = 500
        self.level = 1
        self.attack_speed = 1
        self.attack_range = 1
        
        # Invincibility / damage tracking
        self.invincible = False
        self.invincibility_duration = 0.5
        self.last_hit_time = 0

        # Inventory and animations
        self.inventory = Inventory()
        self.facing_right = True
        self.animation_controller = AnimationController(animations)
        first_animation_frames = next(iter(animations.values()))
        self.frame_width = first_animation_frames[0].get_width()
        self.frame_height = first_animation_frames[0].get_height()
        
        # ----- HITBOX SCALING -----
        # Change this scale to make the collision box smaller/larger.
        HITBOX_SCALE = 1  # 0.6 = 60% of sprite size
        
        # Calculate the smaller hitbox dimensions
        self.hitbox_width = int((self.frame_width * HITBOX_SCALE)/2)
        self.hitbox_height = int((self.frame_height * HITBOX_SCALE)/2)
        
        # Center the smaller hitbox on the player's position
        self.rect = pygame.Rect(
            self.position.x - self.hitbox_width // 2,
            self.position.y + 200,
            self.hitbox_width,
            self.hitbox_height
        )
        
        # Health bar
        self.health_bar = HealthBar(50, 8, (255, 255, 255), (0, 255, 0), (128, 128, 128))
        
        # Buffs dictionary
        self.buffs = {}

        # DEBUG: Toggle this to True if you want to visualize the hitbox
        self.debug_hitbox = False

    def draw(self, screen, camera):
        """
        Draw player sprite and health bar.
        Optionally draw a debug rectangle for the player's smaller hitbox.
        """
        frame = self.animation_controller.get_current_frame(self.facing_right)
        screen_position = camera.apply_to_position(self.position)

        # Draw sprite centered around player's position
        sprite_x = screen_position.x - self.frame_width // 2
        sprite_y = screen_position.y - self.frame_height // 2
        screen.blit(frame, (sprite_x, sprite_y))
        
        # Draw the smaller hitbox if debug is on
        if self.debug_hitbox:
            hitbox_rect_on_screen = camera.apply(self.rect)
            pygame.draw.rect(screen, (255, 0, 0), hitbox_rect_on_screen, 2)

        # Draw health bar above the sprite
        health_bar_position = (screen_position.x - 25, screen_position.y - 40)
        self.health_bar.draw(screen, health_bar_position, self.hp, self.max_hp)

    def update(self, keys):
        self.move(keys)
        self.animation_controller.update_animation()

    def move(self, keys):
        # Decide on animation
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.animation_controller.set_animation("Run")
        else:
            self.animation_controller.set_animation("Idle")

        # Move and flip orientation
        if keys[pygame.K_a]:
            self.position.x -= self.movement_speed
            self.facing_right = False
        if keys[pygame.K_d]:
            self.position.x += self.movement_speed
            self.facing_right = True
        if keys[pygame.K_w]:
            self.position.y -= self.movement_speed
        if keys[pygame.K_s]:
            self.position.y += self.movement_speed

        # Clamp to world boundaries
        self.position.x = max(self.hitbox_width // 2, min(self.position.x, WORLD_WIDTH - self.hitbox_width // 2))
        self.position.y = max(self.hitbox_height // 2, min(self.position.y, WORLD_HEIGHT - self.hitbox_height // 2))

        # Update rect (the smaller hitbox)
        self.rect.topleft = (
            self.position.x - self.hitbox_width // 2,
            self.position.y - self.hitbox_height // 2
        )

    def take_damage(self, damage):
        current_time = pygame.time.get_ticks() / 1000
        if not self.invincible or current_time - self.last_hit_time > self.invincibility_duration:
            self.hp -= damage
            self.last_hit_time = current_time
            self.invincible = True
            self.world.add_floating_text(
                text=str(damage),
                target=self,
                offset=(0, -20),
                color=(255, 0, 0)
            )
            if self.hp <= 0:
                self.die()

    def die(self):
        print("Player has died.")
        self.state_manager.switch_state("end")

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        self.world.add_floating_text(
            text=str(amount),
            target=self,
            offset=(0, -20),
            color=(0, 255, 0)
        )

    def add_buff(self, effect, magnitude, duration):
        self.buffs[effect] = {
            "magnitude": magnitude,
            "end_time": pygame.time.get_ticks() / 1000 + duration
        }
        # Apply the buff now
        if effect == "movement_speed":
            self.movement_speed += magnitude
        elif effect == "damage":
            self.damage += magnitude
        elif effect == "luck":
            self.luck += magnitude
        elif effect == "ability_power":
            self.ability_power += magnitude

    def update_buffs(self):
        current_time = pygame.time.get_ticks() / 1000
        expired_buffs = [effect for effect, data in self.buffs.items() if data["end_time"] <= current_time]
        for effect in expired_buffs:
            magnitude = self.buffs[effect]["magnitude"]
            if effect == "movement_speed":
                self.movement_speed -= magnitude
            elif effect == "damage":
                self.damage -= magnitude
            elif effect == "ability_power":
                self.ability_power -= magnitude
            elif effect == "luck":
                self.luck -= magnitude
            del self.buffs[effect]

    def collect_astral_shard(self):
        """
        Uses 'luck' to determine how many shards are collected each time.
        """
        base_chance = self.luck * 0.05
        guaranteed_multiples = int(base_chance // 1)
        leftover_chance = base_chance % 1

        if random.random() < leftover_chance:
            guaranteed_multiples += 1

        total_multiplier = 1 + guaranteed_multiples
        self.astral_shards += total_multiplier
