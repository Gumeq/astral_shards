import pygame
import time
from settings import *
from src.world import World
from loader import load_player_animations
from src.player import Player
from src.camera import Camera
from src.enemy import EnemyManager, load_enemy_data
from src.weapon import WeaponManager
from src.ui import UI
from src.shop_window import Shop
from src.consumable import ConsumableManager
from src.inventory import Inventory
from src.wave_manager import WaveManager
from src.start_screen import StartScreen  # Your existing StartScreen implementation
from src.game_state_manager import GameStateManager  # New game state manager module
from src.timer import Timer  # Separate timer component
from src.pause_state import PausedState
from src.shop_state import ShopState
# Optional: Add EndScreen if you plan to include it
from src.end_screen import EndScreen

class GamePlay:
    def __init__(self, game_instance, timer):
        self.game = game_instance
        self.timer = timer

    def on_enter(self):
        self.timer.start()

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Switch to paused state
                self.game.state_manager.switch_state("paused")
        
        # After processing special keys, let the Game itself handle movement, shop, etc.
        self.game.handle_events(event_list)

    def update(self):
        self.game.update()

    def render(self, screen):
        self.game.render()



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Astral Shards")
        self.clock = pygame.time.Clock()
        self.running = True

        # Timer
        self.timer = Timer()

        # State Manager
        self.state_manager = GameStateManager()

        # Fonts
        self.font = pygame.font.Font(None, 24)

        # Initialize game objects and states
        self.initialize_game_objects()

        # Register states
        self.state_manager.register_state("start", StartScreen(self.font, self.state_manager))
        self.state_manager.register_state("gameplay", GamePlay(self,self.timer))
        self.state_manager.register_state("paused", PausedState(self.state_manager, self.font, self.timer,self))
        self.state_manager.register_state("shop", ShopState(self))  # <-- Register ShopState here

        # If you implement an end screen, register it here:
        # self.state_manager.register_state("end", EndScreen(self.font, self.state_manager))
        self.state_manager.register_state("end", EndScreen(self.state_manager, self.font,self))

        # Set initial state to "start"
        self.state_manager.switch_state("start")

    def initialize_game_objects(self):
        """Initialize all game objects (world, player, enemies, etc.)."""
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(WIDTH, HEIGHT, self.world.width, self.world.height)

        self.player_animations = load_player_animations()
        self.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, self.player_animations, self.world, self.state_manager)
        self.player.inventory = Inventory()

        self.enemy_data = load_enemy_data("assets/config/enemies.json")
        self.enemy_manager = EnemyManager(self.enemy_data, WORLD_WIDTH, WORLD_HEIGHT, self.world)

        self.wave_manager = WaveManager("assets/config/waves.json", self.world, self.enemy_data, self.enemy_manager, self.camera, self.timer)
        self.wave_manager.start_wave(0)

        self.weapon_manager = WeaponManager("assets/config/weapons.json", self.player)
        basic_wand = self.weapon_manager.weapon_data["basic_wand"]
        self.weapon_manager.equip_weapon("basic_wand")
        self.player.inventory.equip("weapon", basic_wand)

        self.ui = UI(self.font)
        self.consumable_manager = ConsumableManager("assets/config/consumables.json", self.timer)

        self.shop = Shop(self.font, self.player, self.consumable_manager, "assets/config/shop_items.json")
        self.show_detailed_stats = True
        self.elapsed_pause_time = 0
        self.pause_start_time = None
        
    def reset_game(self):
        """
        Reset / re-initialize all game objects to their initial states.
        """
        # If you have code in `initialize_game_objects()`, you can call that here:
        self.initialize_game_objects()
        self.timer.reset()
        self.wave_manager.reset()
        self.wave_manager.start_wave(0)
        # Or manually re-init your objects:
        # self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        # self.player = Player(....)
        # self.enemy_manager = EnemyManager(...)
        # self.timer.reset()
        # etc

    def handle_events(self, event_list):
        """Handle player input events (and pass in the same event_list)."""
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if not self.shop.visible:
                        self.state_manager.switch_state("shop")
                else:
                    # If the shop is not open, process consumable keys
                    if not self.shop.visible:
                        for i in range(5):
                            if keys[pygame.K_1 + i]:
                                self.player.inventory.use_consumable(i, self.player)

        # Let the shop handle its own events if open
        if self.shop.visible:
            for event in event_list:
                self.shop.handle_input(event)
        else:
            # Move the player if the shop is not open
            self.player.update(keys)

            # If firing weapon:
            if mouse_buttons[0]:
                world_mouse_position = pygame.math.Vector2(mouse_position) + self.camera.offset
                self.weapon_manager.fire_weapon(self.player.position, world_mouse_position)


    def update(self):
        """Update game objects."""
        # Update game world and related entities
        self.camera.update(self.player.rect)
        self.world.update()
        self.enemy_manager.update(self.player)
        self.weapon_manager.update(self.enemy_manager.enemies)
        self.player.update_buffs()
        self.player.inventory.update_consumables()
        self.world.check_shard_collection(self.player)
        self.wave_manager.update() 


    def render(self):
        """Render all game objects."""
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        self.enemy_manager.draw(self.screen, self.camera)
        self.weapon_manager.draw(self.screen, self.camera)

        self.ui.draw_inventory(self.screen, self.player.inventory)
        self.ui.draw_shards(self.screen, self.player)
        self.ui.draw_game_time(self.screen, self.timer)


        if self.show_detailed_stats:
            self.ui.draw_stats(self.screen, self.player)

        self.shop.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            event_list = pygame.event.get()  # The single call to pygame.event.get()

            # If you still want to catch QUIT at the top level:
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False

            # State handling: pass event_list to the active state
            self.state_manager.handle_events(event_list)
            self.state_manager.update()
            self.state_manager.render(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
