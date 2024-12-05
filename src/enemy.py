import pygame
from settings import WHITE, GREEN

class Enemy:
    def __init__(self, x, y, hp, damage, image, xp_reward, max_hp, speed=2):
        self.position = pygame.math.Vector2(x, y)
        self.hp = hp
        self.max_hp = max_hp
        self.damage = damage
        self.image = image  # The image for this enemy
        self.rect = self.image.get_rect(center=(x, y))  # Rect for positioning
        self.xp_reward = xp_reward
        self.speed = speed  # Enemy speed

    def move_towards_player(self, player):
        direction = player.position - self.position
        if direction.length() != 0:
            direction.normalize_ip()
            self.position += direction * self.speed
            self.rect.center = self.position

    def draw(self, screen):
        # Draw the enemy image
        screen.blit(self.image, self.rect.topleft)

        # Draw health bar above the enemy
        pygame.draw.rect(screen, WHITE, (self.rect.centerx - 20, self.rect.top - 10, 40, 5))  # Background
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - 20, self.rect.top - 10, 40 * (self.hp / self.max_hp), 5))  # Current HP
