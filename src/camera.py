from settings import *
import pygame

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pygame.math.Vector2(0, 0)  # Camera offset

    def update(self, target_rect):
        """
        Update the camera offset based on the target (e.g., player).
        Keeps the target centered while respecting world bounds.
        """
        self.offset.x = max(0, min(target_rect.centerx - self.screen_width // 2, self.world_width - self.screen_width))
        self.offset.y = max(0, min(target_rect.centery - self.screen_height // 2, self.world_height - self.screen_height))

    def apply(self, rect):
        """
        Apply the camera offset to a rectangle, returning its position on the screen.
        """
        return rect.move(-self.offset.x, -self.offset.y)

    def apply_to_position(self, position):
        """
        Apply the camera offset to a position, returning its position on the screen.
        """
        return position - self.offset
