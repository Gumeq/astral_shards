import pygame
from settings import *
from src.world import World
from loader import (
    load_player_animations,
)
from src.player import Player
from src.camera import Camera
from src.enemy import EnemyManager, load_enemy_data
from src.weapon import WeaponManager
from src.ui import UI
from src.shop_window import Shop
from src.consumable import ConsumableManager
from src.inventory import Inventory
from src.wave_manager import WaveManager
from src.start_screen import StartScreen  # Make sure you have a StartScreen class implemented

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Astral Shards")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_paused = False
        
        # Initialize shared game state
        self.game_state = {
            "current_wave_index": 0,
            "running": True,
        }

        self.start_time = pygame.time.get_ticks() / 1000

        # Initialize World, Player, and Camera
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(WIDTH, HEIGHT, self.world.width, self.world.height)

        self.player_animations = load_player_animations()
        self.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, self.player_animations, self.world)
        self.player.inventory = Inventory()

        self.enemy_data = load_enemy_data("assets/config/enemies.json")
        self.enemy_manager = EnemyManager(self.enemy_data, WORLD_WIDTH, WORLD_HEIGHT, self.world)

        # Waves
        self.wave_manager = WaveManager("assets/config/waves.json", self.world, self.enemy_data, self.enemy_manager, self.camera)
        self.wave_manager.start_wave(0)

        # Equip a weapon
        self.weapon_manager = WeaponManager("assets/config/weapons.json", self.player)
        basic_wand = self.weapon_manager.weapon_data["basic_wand"]
        self.weapon_manager.equip_weapon("basic_wand")
        self.player.inventory.equip("weapon", basic_wand)

        # Initialize UI
        self.font = pygame.font.Font(None, 24)  # Default font for UI
        self.small_font = pygame.font.Font(None, 24)  # Font for the shop
        self.ui = UI(self.font)

        # Initialize consumables
        self.consumable_manager = ConsumableManager("assets/config/consumables.json")

        self.dropped_shards = []

        # Initialize Shop
        self.shop = Shop(self.small_font, self.player, self.consumable_manager, "assets/config/shop_items.json")
        
        self.show_detailed_stats = False

    def start(self):
        """Show the start screen before running the game."""
        # Create a StartScreen instance
        start_screen = StartScreen(self.font)
        # Display the start screen. If returns False, user quit; if True, proceed.
        start_game = start_screen.show(self.screen)
        if not start_game:
            # User quit from start screen
            self.running = False

    def handle_events(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Toggle shop with B in the game class only
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.shop.toggle()
                self.game_paused = self.shop.visible

            if self.shop.visible:
                # Send events to shop, but don't toggle shop again inside Shop
                self.shop.handle_input(event)
                self.game_paused = self.shop.visible
            else:
                # Handle other inputs only if shop is not visible
                if event.type == pygame.KEYDOWN:
                    # Use consumables with keys 1-5
                    for i in range(5):
                        if keys[pygame.K_1 + i]:
                            self.player.inventory.use_consumable(i, self.player)

        self.show_detailed_stats = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

        # Update player movement if shop not visible
        if not self.shop.visible:
            self.player.update(keys)
        if mouse_buttons[0]:
            world_mouse_position = pygame.math.Vector2(mouse_position) + self.camera.offset
            self.weapon_manager.fire_weapon(self.player.position, world_mouse_position)

    def update(self):
        if self.game_paused:
            return
        
        self.camera.update(self.player.rect)
        self.world.update()
        self.enemy_manager.update(self.player)
        self.weapon_manager.update(self.enemy_manager.enemies)
        self.player.update_buffs()
        self.player.inventory.update_consumables()
        self.world.check_shard_collection(self.player)
        self.wave_manager.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        self.enemy_manager.draw(self.screen, self.camera)
        self.weapon_manager.draw(self.screen, self.camera)

        # Draw UI
        self.ui.draw_inventory(self.screen, self.player.inventory)
        self.ui.draw_shards(self.screen, self.player)
        # Pass game_paused if your UI timer needs it, or modify accordingly
        self.ui.draw_game_time(self.screen, self.start_time, self.game_paused)

        if self.show_detailed_stats:
            self.ui.draw_stats(self.screen, self.player)

        # Draw shop if visible
        self.shop.draw(self.screen)

        pygame.display.flip()

    def start_game(self):
        self.wave_manager.start_wave(3)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()


# In your main script:
# if __name__ == "__main__":
#     game = Game()
#     game.start()  # show the start screen
#     if game.running:
#         game.run()  # only run if start screen wasn't quit
