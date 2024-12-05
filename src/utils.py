import pygame
from settings import WHITE

def check_collision(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect)

class FloatingText:
    def __init__(self, x, y, text, color=WHITE, duration=30):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.duration = duration  # Frames the text is visible

    def draw(self, screen, font):
        if self.duration > 0:
            rendered_text = font.render(self.text, True, self.color)
            screen.blit(rendered_text, (self.x, self.y))
            self.y -= 1  # Make the text float upward
            self.duration -= 1
