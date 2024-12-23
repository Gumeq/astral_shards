import pygame

class ShopState:
    """The state when the player opens the shop."""

    def __init__(self, game_instance):
        self.game = game_instance
        # We can rely on self.game.shop to access the Shop object
        # This also lets us draw gameplay behind the shop if we want

    def on_enter(self):
        """Called when we switch to the ShopState."""
        # Make sure the Shop is marked visible
        self.game.shop.visible = True
        self.game.timer.stop()

    def handle_events(self, event_list):
        """Handle shop-specific events."""
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # Let the user close the shop using 'B' or 'Esc'
                if event.key in (pygame.K_b, pygame.K_ESCAPE):
                    self.game.shop.visible = False
                    # Switch back to gameplay
                    self.game.state_manager.switch_state("gameplay")
                else:
                    # Otherwise, let the shop handle its own input
                    self.game.shop.handle_input(event)

    def update(self):
        """No gameplay updates happen here, so it's effectively 'paused'."""
        pass

    def render(self, screen):
        """Render the gameplay behind the shop, then draw the shop."""
        # 1. Draw the current gameplay state behind the shop
        #    If you want to keep showing the world behind the shop,
        #    you can do something like the line below:
        self.game.render()
