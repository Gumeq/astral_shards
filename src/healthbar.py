import pygame

class HealthBar:
    def __init__(self, width, height, border_color, fill_color, background_color):
        self.width = width
        self.height = height
        self.border_color = border_color
        self.fill_color = fill_color
        self.background_color = background_color

    def draw(self, screen, position, current_hp, max_hp):
        """Draw the health bar on the screen."""
        # Calculate the health bar's fill width based on the current health
        fill_width = int(self.width * (current_hp / max_hp))

        # Draw the background of the health bar
        background_rect = pygame.Rect(position[0], position[1], self.width, self.height)
        pygame.draw.rect(screen, self.background_color, background_rect)

        # Draw the filled portion of the health bar
        fill_rect = pygame.Rect(position[0], position[1], fill_width, self.height)
        pygame.draw.rect(screen, self.fill_color, fill_rect)

        # Draw the border around the health bar
        pygame.draw.rect(screen, self.border_color, background_rect, 1)
