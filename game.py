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
from src.start_screen import StartScreen
from src.game_state_manager import GameStateManager
from src.timer import Timer
from src.pause_state import PausedState
from src.shop_state import ShopState
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
                self.game.state_manager.switch_state("paused")
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
        self.timer = Timer()
        self.state_manager = GameStateManager()
        self.font = pygame.font.Font("assets/fonts/dogicapixel.ttf", 16)
        self.initialize_game_objects()
        self.state_manager.register_state("start", StartScreen(self.font, self.state_manager))
        self.state_manager.register_state("gameplay", GamePlay(self, self.timer))
        self.state_manager.register_state("paused", PausedState(self.state_manager, self.font, self.timer, self))
        self.state_manager.register_state("shop", ShopState(self))
        self.state_manager.register_state("end", EndScreen(self.state_manager, self.font, self, self.player))
        self.state_manager.switch_state("start")

    def initialize_game_objects(self):
        # Load animations and data first
        self.player_animations = load_player_animations()
        self.enemy_data = load_enemy_data("assets/config/enemies.json")
        
        # Initialize Player without the world reference
        self.player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, self.player_animations, None, self.state_manager)
        
        # Initialize World without the player reference
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, None, self.timer)
        
        # Resolve the circular dependency
        self.world.player = self.player
        self.player.world = self.world
        
        # Initialize Camera after World is initialized
        self.camera = Camera(WIDTH, HEIGHT, self.world.width, self.world.height)
        
        # Continue initializing the remaining game objects
        self.player.inventory = Inventory()
        self.enemy_manager = EnemyManager(self.enemy_data, WORLD_WIDTH, WORLD_HEIGHT, self.world)
        self.wave_manager = WaveManager("assets/config/waves.json", self.world, self.enemy_data, self.enemy_manager, self.camera, self.timer)
        self.wave_manager.start_wave(0)
        
        # Initialize and equip weapons
        self.weapon_manager = WeaponManager("assets/config/weapons.json", self.player, self.world.projectiles)
        basic_wand = self.weapon_manager.weapon_data["basic_wand"]
        self.weapon_manager.equip_weapon("basic_wand")
        self.player.inventory.equip("weapon", basic_wand)
        
        # UI and other managers
        self.ui = UI(self.font, self.wave_manager)
        self.consumable_manager = ConsumableManager("assets/config/consumables.json", self.timer)
        self.shop = Shop(self.font, self.player, self.consumable_manager, "assets/config/shop_items.json")
        
        # Game state tracking
        self.show_detailed_stats = True
        self.elapsed_pause_time = 0
        self.pause_start_time = None


    def reset_game(self):
        self.initialize_game_objects()
        self.timer.reset()
        self.wave_manager.reset()
        self.wave_manager.start_wave(0)

    def handle_events(self, event_list):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if not self.shop.visible:
                        self.state_manager.switch_state("shop")
                elif not self.shop.visible:
                    for i in range(5):
                        if keys[pygame.K_1 + i]:
                            self.player.inventory.use_consumable(i, self.player)
        if self.shop.visible:
            for event in event_list:
                self.shop.handle_input(event)
        else:
            self.player.update(keys)
            if True:
                world_mouse_position = pygame.math.Vector2(mouse_position) + self.camera.offset
                self.weapon_manager.fire_weapon(self.player.position, world_mouse_position)

    def update(self):
        self.camera.update(self.player.rect)
        self.world.update()
        self.enemy_manager.update(self.player, self.timer)
        self.weapon_manager.update(self.world.enemies)
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
        self.ui.draw_inventory(self.screen, self.player.inventory)
        self.ui.draw_shards(self.screen, self.player)
        self.ui.draw_game_time(self.screen, self.timer)
        if self.show_detailed_stats:
            self.ui.draw_stats(self.screen, self.player)
        self.shop.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False
            self.state_manager.handle_events(event_list)
            self.state_manager.update()
            self.state_manager.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
