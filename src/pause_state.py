import pygame

class PausedState:
    def __init__(self, state_manager, font, timer, game):
        self.state_manager = state_manager
        self.timer = timer
        self.game = game
        self.font = font
        self.large_font = pygame.font.Font(None, 48)

    def on_enter(self):
        self.timer.stop()

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state_manager.switch_state("gameplay")
                elif event.key == pygame.K_x:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    self.state_manager.switch_state("start")
                    self.game.reset_game()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.draw(screen)

    def draw(self, screen):
        WIDTH, HEIGHT = screen.get_size()
        title_text = self.large_font.render("Game Paused", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        instructions = ["Press ESC to Resume", "Press R to Restart", "Press X to Quit"]
        y_offset = title_rect.bottom + 50

        for instr in instructions:
            instr_surface = self.font.render(instr, True, (200, 200, 200))
            instr_rect = instr_surface.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(instr_surface, instr_rect)
            y_offset += 30
