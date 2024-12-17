import pygame
from settings import *
from src.healthbar import HealthBar
from src.inventory import Inventory

class AnimationController:
    def __init__(self, animations, animation_speed=10):
        self.animations = animations  # Dictionary of animations
        self.current_animation = "Idle"  # Default animation
        self.current_frame = 0
        self.animation_speed = animation_speed  # Frames per second
        self.last_update = pygame.time.get_ticks()

    def set_animation(self, animation_name):
        """Switch to a new animation."""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0

    def update_animation(self):
        """Update the animation frame based on time."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

    def get_current_frame(self, facing_right=True):
        """Get the current animation frame."""
        frame = self.animations[self.current_animation][self.current_frame]
        if not facing_right:
            frame = pygame.transform.flip(frame, True, False)
        return frame


class Player:
    def __init__(self, x, y, animations, world):
        self.world = world
        self.position = pygame.math.Vector2(x, y)
        self.movement_speed = 5
        self.ability_power = 20
        self.hp = 100
        self.max_hp = 150
        self.luck = 1
        self.astral_shards = 50
        self.level = 1
        self.attack_speed = 1
        self.attack_range = 1
        self.invincible = False
        self.invincibility_duration = 1  # Seconds
        self.last_hit_time = 0
        self.inventory = Inventory()
        self.facing_right = True  # Default facing direction
        # Initialize animation controller
        self.animation_controller = AnimationController(animations)
        # Dimensions and hitbox
        first_animation_frames = next(iter(animations.values()))
        self.frame_width = first_animation_frames[0].get_width()
        self.frame_height = first_animation_frames[0].get_height()
        self.rect = pygame.Rect(
            self.position.x - self.frame_width // 2,
            self.position.y - self.frame_height // 2,
            self.frame_width,
            self.frame_height
        )
        self.health_bar = HealthBar(
            width=50,  # Fixed width
            height=8,  # Height of the health bar
            border_color=(255, 255, 255),  # White border
            fill_color=(0, 255, 0),  # Green fill
            background_color=(128, 128, 128)  # Gray background
        )
        
        self.buffs = {}
    def draw(self, screen, camera):
        """Draw the player and their health bar."""
        frame = self.animation_controller.get_current_frame(self.facing_right)
        screen_position = camera.apply_to_position(self.position)
        screen.blit(frame, (screen_position.x - self.rect.width // 2, screen_position.y - self.rect.height // 2))

        # Draw health bar above the player
        health_bar_position = (screen_position.x - 25, screen_position.y - 40)
        self.health_bar.draw(screen, health_bar_position, self.hp, self.max_hp)
        
    def update(self, keys):
        """Update player position and animation."""
        self.move(keys)
        self.animation_controller.update_animation()

    def move(self, keys):
        """Update player position based on input and set facing direction."""
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.animation_controller.set_animation("Run")
        else:
            self.animation_controller.set_animation("Idle")
        if keys[pygame.K_a]:  # Move left
            self.position.x -= self.movement_speed
            self.facing_right = False  # Facing left
        if keys[pygame.K_d]:  # Move right
            self.position.x += self.movement_speed
            self.facing_right = True  # Facing right
        if keys[pygame.K_w]:  # Move up
            self.position.y -= self.movement_speed
        if keys[pygame.K_s]:  # Move down
            self.position.y += self.movement_speed

        # Ensure the player stays within world bounds
        self.position.x = max(self.frame_width // 2, min(self.position.x, WORLD_WIDTH - self.frame_width // 2))
        self.position.y = max(self.frame_height // 2, min(self.position.y, WORLD_HEIGHT - self.frame_height // 2))

        # Update the player's rectangle position
        self.rect.topleft = (self.position.x - self.frame_width // 2, self.position.y - self.frame_height // 2)

    def take_damage(self, damage):
            """Reduce the player's health if not invincible."""
            current_time = pygame.time.get_ticks() / 1000  # Time in seconds
            if not self.invincible or current_time - self.last_hit_time > self.invincibility_duration:
                self.hp -= damage
                self.last_hit_time = current_time
                self.invincible = True
                self.world.add_floating_text(
                            text=str(damage),
                            target = self,
                            offset=(0, -20),  # Slightly above the player
                            color=(255, 0, 0),  # Red for damage
                        )
                if self.hp <= 0:
                    self.die()

    def die(self):
        """Handle player death."""
        print("Player has died.")

    def heal(self, amount):
        """Heal the player."""
        self.hp = min(self.hp + amount, self.max_hp)  # Ensure HP doesn't go above max HP
        self.world.add_floating_text(
                    text=str(amount),
                    target = self,
                    offset=(0, -20),  # Slightly above the player
                    color=(0, 255, 0),  # Red for damage
                )
        
    def add_buff(self, effect, magnitude, duration):
        """Add a buff to the player."""
        self.buffs[effect] = {
            "magnitude": magnitude,
            "end_time": pygame.time.get_ticks() / 1000 + duration
        }
        if effect == "movement_speed":
            self.movement_speed += magnitude
        elif effect == "damage":
            self.damage += magnitude
        elif effect == "luck":
            self.luck += magnitude

    def update_buffs(self):
        """Remove expired buffs."""
        current_time = pygame.time.get_ticks() / 1000
        expired_buffs = [effect for effect, data in self.buffs.items() if data["end_time"] <= current_time]
        for effect in expired_buffs:
            magnitude = self.buffs[effect]["magnitude"]
            if effect == "movement_speed":
                self.movement_speed -= magnitude
            elif effect == "damage":
                self.damage -= magnitude
            elif effect == "luck":
                self.luck -= magnitude
            del self.buffs[effect]


    def collect_astral_shard(self):
        self.astral_shards +=1
        
