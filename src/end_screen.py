import pygame

class EndScreen:
    def __init__(self, state_manager, font, game, player):
        self.state_manager = state_manager
        self.font = font
        self.game = game

    def on_enter(self):
        pass

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state_manager.switch_state("start")
                    self.game.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        text_surface = self.font.render("GAME OVER!", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        screen.blit(text_surface, text_rect)
        smaller_text = self.font.render("Press R to restart or ESC to quit.", True, (255, 255, 255))
        smaller_rect = smaller_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
        screen.blit(smaller_text, smaller_rect)
