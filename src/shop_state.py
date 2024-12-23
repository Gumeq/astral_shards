import pygame

class ShopState:
    def __init__(self, game_instance):
        self.game = game_instance

    def on_enter(self):
        self.game.shop.visible = True
        self.game.timer.stop()

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_b, pygame.K_ESCAPE):
                    self.game.shop.visible = False
                    self.game.state_manager.switch_state("gameplay")
                else:
                    self.game.shop.handle_input(event)

    def update(self):
        pass

    def render(self, screen):
        self.game.render()
