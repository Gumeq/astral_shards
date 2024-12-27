import pygame

class HealthBar:
    def __init__(self, width, height, border_color, fill_color, background_color):
        self.width = width
        self.height = height
        self.border_color = border_color
        self.fill_color = fill_color
        self.background_color = background_color

    def draw(self, screen, position, current_hp, max_hp):
        fill_width = int(self.width * (current_hp / max_hp))
        background_rect = pygame.Rect(position[0], position[1], self.width, self.height)
        pygame.draw.rect(screen, self.background_color, background_rect)
        fill_rect = pygame.Rect(position[0], position[1], fill_width, self.height)
        pygame.draw.rect(screen, self.fill_color, fill_rect)
        pygame.draw.rect(screen, self.border_color, background_rect, 1)