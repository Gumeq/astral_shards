import pygame
from settings import RED, BLUE, GREEN, WHITE, WIDTH, HEIGHT

class Player:
    def __init__(self, x, y, animations):
        self.position = pygame.math.Vector2(x, y)
        self.speed = 5
        self.magic = 5
        self.hp = 100
        self.max_hp = 100
        self.luck = 1
        self.xp = 0
        self.level = 1
        self.next_level_xp = 15
        self.attack_speed = 1
        self.damage = 50
        self.fire_rate = 500  # milliseconds between shots
        self.inventory = []
        self.special_ability = False
        self.animations = animations  # Dictionary of animations
        self.current_animation = "Idle"  # Default animation
        self.current_frame = 0
        self.animation_speed = 10  # Frames per second
        self.last_update = pygame.time.get_ticks()
        self.facing_right = True  # Default facing direction
        first_animation_frames = next(iter(animations.values()))
        self.frame_width = first_animation_frames[0].get_width()
        self.frame_height = first_animation_frames[0].get_height()
        self.rect = pygame.Rect(
            self.position.x - self.frame_width // 2,
            self.position.y - self.frame_height // 2,
            self.frame_width,
            self.frame_height
        )

    @staticmethod
    def _load_frames(sprite_sheet, num_frames, frame_height):
        """Extract frames from the sprite sheet based on the number of frames and frame height."""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width = sheet_width // num_frames
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sprite_sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        return frames

    def set_animation(self, animation_name):
        """Switch to a new animation."""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            # Update frame dimensions
            self.frame_width = self.animations[animation_name][0].get_width()
            self.frame_height = self.animations[animation_name][0].get_height()

    def update_animation(self):
        """Update the animation frame based on time."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])

    def draw(self, screen):
        """Draw the player using the current animation frame."""
        frame = self.animations[self.current_animation][self.current_frame]
        
        # Flip the frame if the player is facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        screen.blit(frame, (self.position.x - self.frame_width // 2, self.position.y - self.frame_height // 2))

        # Draw health bar above the player
        pygame.draw.rect(screen, WHITE, (self.position.x - 40, self.position.y - 50, 80, 8))  # Background
        pygame.draw.rect(screen, GREEN, (self.position.x - 40, self.position.y - 50, 80 * (self.hp / self.max_hp), 8))

    def move(self, keys):
        """Update player position based on input and set facing direction."""
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.set_animation("Run")
        else:
            self.set_animation("Idle")

        if keys[pygame.K_a]:  # Move left
            self.position.x -= self.speed
            self.facing_right = False  # Facing left
        if keys[pygame.K_d]:  # Move right
            self.position.x += self.speed
            self.facing_right = True  # Facing right
        if keys[pygame.K_w]:  # Move up
            self.position.y -= self.speed
        if keys[pygame.K_s]:  # Move down
            self.position.y += self.speed

        # Ensure the player stays within screen bounds
        self.position.x = max(self.frame_width // 2, min(self.position.x, WIDTH - self.frame_width // 2))
        self.position.y = max(self.frame_height // 2, min(self.position.y, HEIGHT - self.frame_height // 2))

        # Update the player's rectangle position
        self.rect.topleft = (self.position.x - self.frame_width // 2, self.position.y - self.frame_height // 2)

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)  # Ensure HP doesn't go below 0
        self.set_animation("Hurt")
        if self.hp == 0:
            self.set_animation("Dead")

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)  # Ensure HP doesn't go above max HP

    def apply_item_effect(self, item):
        if item.item_type == "hp":
            self.heal(item.value)
        elif item.item_type == "damage":
            self.damage += item.value
        elif item.item_type == "fire_rate":
            self.fire_rate = max(self.fire_rate - item.value, 1)
        self.inventory.append(item)  # Add the item to the inventory
