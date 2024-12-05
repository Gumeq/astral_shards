# item.py
import pygame

class Item:
    def __init__(self, x, y, item_type, image, effect):
        self.position = pygame.math.Vector2(x, y)
        self.item_type = item_type
        self.image = image
        self.rect = self.image.get_rect(center=self.position)
        self.effect = effect

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def apply_effect(self, player):
        self.effect(player)
