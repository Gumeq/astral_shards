import pygame
import random

class FloatingText:
    def __init__(self, text, target, offset, color, duration=1, font=None):
        self.text = text
        self.target = target
        self.offset = pygame.math.Vector2(offset)
        self.color = color
        self.duration = duration
        self.start_time = pygame.time.get_ticks() / 1000
        self.font = pygame.font.Font("assets/fonts/dogicabold.ttf", 24)
        self.random_movement = pygame.math.Vector2(
            random.uniform(-0.5, 0.5),
            random.uniform(-0.2, -0.5)
        )

    def update(self):
        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - self.start_time
        self.offset += self.random_movement
        return elapsed_time >= self.duration

    def draw(self, screen, camera=None):
        position = pygame.math.Vector2(self.target.position) + self.offset if self.target else self.offset
        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - self.start_time
        alpha = max(0, int(255 * (1 - elapsed_time / self.duration)))
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=position)
        if camera:
            text_rect.topleft -= camera.offset
        screen.blit(text_surface, text_rect.topleft)
