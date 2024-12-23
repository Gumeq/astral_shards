import pygame

class PausedState:
    def __init__(self, state_manager, font, timer,game):
        self.state_manager = state_manager
        self.timer = timer
        self.game = game
        self.font = font
        self.large_font = pygame.font.Font(None, 48)  # For the title

    def on_enter(self):
        """Called when entering the paused state."""
        self.timer.stop()


    def handle_events(self, event_list):
        """Handle user input events for the paused state."""
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Resume game on 'P'
                    self.state_manager.switch_state("gameplay")
                elif event.key == pygame.K_x:  # Quit game
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    # Go back to the start screen (or gameplay directly)
                    self.state_manager.switch_state("start")
                    self.game.reset_game()

    def update(self):
        """No updates needed in paused state."""
        pass

    def render(self, screen):
        """Render the paused state."""
        screen.fill((0, 0, 0))
        self.draw(screen)

    def draw(self, screen):
        WIDTH, HEIGHT = screen.get_size()

        # Pause title
        title_text = self.large_font.render("Game Paused", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Press ESC to Resume",
            "Press R to Restart",
            "Press X to Quit",
        ]

        y_offset = title_rect.bottom + 50
        for instr in instructions:
            instr_surface = self.font.render(instr, True, (200, 200, 200))
            instr_rect = instr_surface.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(instr_surface, instr_rect)
            y_offset += 30
