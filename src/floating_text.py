import pygame
import random

class FloatingText:
    def __init__(self, text, target, offset, color, duration=1, font=None):
        """
        Initialize floating text.
        :param text: Text to display
        :param target: The object (e.g., player, enemy) the text follows
        :param offset: Offset relative to the target's position
        :param color: Text color
        :param duration: How long the text lasts (in seconds)
        :param font: Font for the text
        """
        self.text = text
        self.target = target
        self.offset = pygame.math.Vector2(offset)
        self.color = color
        self.duration = duration  # How long the text lasts (in seconds)
        self.start_time = pygame.time.get_ticks() / 1000  # Record the start time
        self.font = font or pygame.font.Font(None, 24)  # Default font

        # Randomized movement
        self.random_movement = pygame.math.Vector2(
            random.uniform(-0.5, 0.5),  # Horizontal sway
            random.uniform(-0.2, -0.5)  # Slight upward bias
        )

    def update(self):
        """Update the floating text's position and check if it should disappear."""
        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - self.start_time

        # Apply randomized movement
        self.offset += self.random_movement

        # Return True if the text's duration has expired
        return elapsed_time >= self.duration

    def draw(self, screen, camera=None):
        """Draw the floating text on the screen with a fade-out effect."""
        # Calculate position relative to the target
        if self.target:
            position = pygame.math.Vector2(self.target.position) + self.offset
        else:
            position = self.offset

        # Calculate alpha for fade-out effect
        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - self.start_time
        alpha = max(0, int(255 * (1 - elapsed_time / self.duration)))  # Linear fade-out

        # Render the text with fading color
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)

        text_rect = text_surface.get_rect(center=position)

        # Apply camera offset if provided (for world positioning)
        if camera:
            text_rect.topleft -= camera.offset

        screen.blit(text_surface, text_rect.topleft)
