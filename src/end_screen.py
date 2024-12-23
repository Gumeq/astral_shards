import pygame

class EndScreen:
    def __init__(self, state_manager, font, game):
        self.state_manager = state_manager
        self.font = font
        self.game = game

    def on_enter(self):
        """Called when we switch to the EndScreen state."""
        # You might want to stop your game timer here, play a sound, etc.
        pass

    def handle_events(self, event_list):
        """Handle input events on the end screen."""
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # For example, press "R" to restart, or "ESC" to quit.
                if event.key == pygame.K_r:
                    # Go back to the start screen (or gameplay directly)
                    self.state_manager.switch_state("start")
                    self.game.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    # Quit the game
                    pygame.quit()
                    raise SystemExit

    def update(self):
        """No updates needed if it's a static screen, but you could animate something here."""
        pass

    def render(self, screen):
        """Draw the 'Game Over' text and any other info."""
        screen.fill((0, 0, 0))  # Fill background with black

        # Render "Game Over" or "You Died" text
        text_surface = self.font.render("GAME OVER!", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        screen.blit(text_surface, text_rect)

        # Maybe show instructions for restarting or quitting
        smaller_text = self.font.render("Press R to restart or ESC to quit.", True, (255, 255, 255))
        smaller_rect = smaller_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(smaller_text, smaller_rect)
