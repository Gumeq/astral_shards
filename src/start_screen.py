import pygame
import time
import math

class StartScreen:
    def __init__(self, font, state_manager):
        self.font = font
        self.large_font = pygame.font.Font(None, 48)  # For the title
        self.running = True
        self.start_button_rect = None
        self.start_time = time.time()
        self.state_manager = state_manager  # Reference to the state manager

    def on_enter(self):
        """Called when entering the start state."""
        self.running = True  # Reset the running flag

    def handle_events(self, event_list):
        """Handle user input events for the start screen."""
        for event in event_list:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Pressing Enter or Space starts the game
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.running = False
                    self.state_manager.switch_state("gameplay")  # Switch to gameplay state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if user clicked on the start button
                if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                    self.running = False
                    self.state_manager.switch_state("gameplay")  # Switch to gameplay state

    def update(self):
        """Perform any updates needed for the start screen."""
        pass

    def render(self, screen):
        """Render the start screen."""
        screen.fill((0, 0, 0))
        self.draw(screen)

    def draw(self, screen):
        WIDTH, HEIGHT = screen.get_size()

        # Title
        title_text = self.large_font.render("Astral Shards", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Movement: W A S D",
            "Open Shop: B",
            "Use Items: 1-5",
            "Press Enter or Click the button below to start."
        ]

        y_offset = title_rect.bottom + 50
        for instr in instructions:
            instr_surface = self.font.render(instr, True, (200, 200, 200))
            instr_rect = instr_surface.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(instr_surface, instr_rect)
            y_offset += 30

        # Draw the start button with a bouncing animation
        button_text = "Start Game"
        button_surface = self.font.render(button_text, True, (255, 255, 255))
        
        # Simple bounce animation:
        elapsed = time.time() - self.start_time
        bounce = math.sin(elapsed * 2) * 5  # Sine wave for bounce (2 Hz, 5 pixels amplitude)

        button_width = button_surface.get_width() + 40
        button_height = button_surface.get_height() + 20

        button_x = (WIDTH - button_width) // 2
        button_y = y_offset + 50 + int(bounce)  # Add bounce to vertical position

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (50, 50, 50), button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)

        # Center the text inside the button
        text_x = button_rect.centerx - button_surface.get_width() // 2
        text_y = button_rect.centery - button_surface.get_height() // 2
        screen.blit(button_surface, (text_x, text_y))

        self.start_button_rect = button_rect

