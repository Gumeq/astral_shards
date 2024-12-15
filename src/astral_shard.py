import pygame

class AstralShard:
    def __init__(self, x, y,size=(32,32)):
        """Initialize the Astral Shard object."""
        self.position = pygame.math.Vector2(x, y)
        original_image = pygame.image.load("assets/images/items/astral_shard.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen, camera):
        """Draw the Astral Shard on the screen."""
        screen_position = camera.apply(self.rect)
        screen.blit(self.image, screen_position.topleft)
