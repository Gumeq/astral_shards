# game.py
import pygame
import random
import math
from settings import WIDTH, HEIGHT, FPS, WHITE, RED
from src.player import Player
from src.projectile import Projectile
from src.enemy import Enemy
from src.utils import check_collision, FloatingText
from src.item import Item
from src.hud import draw_hud
from settings import ENEMY_WAVES
from loader import (
    load_enemy_images,
    load_projectile_sprite,
    load_item_factory,
    load_player_animations
)
from level_up_system import level_up

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Astral Shards")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True

        # Load assets
        self.enemy_images = load_enemy_images()
        self.projectile_sprite_sheet = load_projectile_sprite()
        self.item_factory = load_item_factory()  # Initialize the item factory
        self.player_animations = load_player_animations()
        self.background_tile = pygame.image.load("assets/images/backgrounds/tile_1.webp").convert()  # Load the background tile image

        # Initialize game objects
        self.player = Player(400, 300, self.player_animations)
        self.projectiles = []
        self.enemies = []
        self.items = []
        self.floating_texts = []

        # Game state variables
        self.last_shot = pygame.time.get_ticks()
        self.player_damage_cooldown = 0
        self.damage_interval = 30
        self.current_wave_index = 0
        self.wave_start_time = pygame.time.get_ticks()

        # Projectile animation parameters
        self.projectile_num_frames = 12
        self.projectile_frame_height = 64

    def draw_inventory(self):
        x, y = 10, 220
        for i, item in enumerate(self.player.inventory):
            text = self.font.render(f"Item {i + 1}: {item.item_type} +{item.value}", True, WHITE)
            self.screen.blit(text, (x, y + i * 20))

    def handle_events(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_player(self):
        self.player.move(self.keys)
        self.player.update_animation()

    def shoot_projectiles(self):
        if self.mouse_buttons[0]:
            if pygame.time.get_ticks() - self.last_shot > self.player.fire_rate:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.player.special_ability:
                    self.fire_triple_shot(mouse_x, mouse_y)
                else:
                    self.fire_single_shot(mouse_x, mouse_y)
                self.last_shot = pygame.time.get_ticks()

    def fire_single_shot(self, mouse_x, mouse_y):
        projectile = Projectile(
            self.player.position.x,
            self.player.position.y,
            mouse_x,
            mouse_y,
            self.projectile_sprite_sheet,
            self.projectile_num_frames,
            self.projectile_frame_height
        )
        self.projectiles.append(projectile)

    def fire_triple_shot(self, mouse_x, mouse_y):
        angle_offset = 15  # Degrees
        offset_radians = math.radians(angle_offset)
        direction = pygame.math.Vector2(mouse_x - self.player.position.x, mouse_y - self.player.position.y)
        if direction.length() != 0:
            direction.normalize_ip()
        base_angle = math.atan2(direction.y, direction.x)
        angles = [base_angle - offset_radians, base_angle, base_angle + offset_radians]
        for angle in angles:
            dx = math.cos(angle)
            dy = math.sin(angle)
            target_x = self.player.position.x + dx * 1000
            target_y = self.player.position.y + dy * 1000
            projectile = Projectile(
                self.player.position.x,
                self.player.position.y,
                target_x,
                target_y,
                self.projectile_sprite_sheet,
                self.projectile_num_frames,
                self.projectile_frame_height
            )
            self.projectiles.append(projectile)

    def update_projectiles(self):
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            projectile.update_animation()
            if projectile.is_expired():
                projectiles_to_remove.append(projectile)
                continue
            if not projectile.hit_enemy:
                for enemy in self.enemies:
                    if check_collision(projectile, enemy):
                        enemy.hp -= self.player.damage
                        self.floating_texts.append(FloatingText(enemy.position.x, enemy.position.y - 20, f"-{self.player.damage}", RED))
                        projectile.hit_enemy = True
                        projectile.moving = False
                        projectile.current_frame = 4
                        if enemy.hp <= 0:
                            self.enemies.remove(enemy)
                            self.player.xp += enemy.xp_reward
                            self.spawn_item(enemy)
                        break
        for projectile in projectiles_to_remove:
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)

    def spawn_item(self, enemy):
        if random.random() < 0.25 * self.player.luck:
            item_type = random.choice(list(self.item_factory.item_data.keys()))
            item = self.item_factory.create_item(enemy.position.x, enemy.position.y, item_type)
            self.items.append(item)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
            if check_collision(self.player, enemy) and self.player_damage_cooldown == 0:
                self.player.take_damage(enemy.damage)
                self.player_damage_cooldown = self.damage_interval
        if self.player_damage_cooldown > 0:
            self.player_damage_cooldown -= 1

    def draw_game_elements(self):
        # Draw background tiles
        for x in range(0, WIDTH, self.background_tile.get_width()):
            for y in range(0, HEIGHT, self.background_tile.get_height()):
                self.screen.blit(self.background_tile, (x, y))
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        # Draw items
        for item in self.items[:]:
            item.draw(self.screen)
            if check_collision(self.player, item):
                self.player.apply_item_effect(item)
                self.items.remove(item)
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        # Draw player
        self.player.draw(self.screen)
        # Draw floating texts
        for floating_text in self.floating_texts[:]:
            floating_text.draw(self.screen, self.font)
            if floating_text.duration <= 0:
                self.floating_texts.remove(floating_text)
        # Draw HUD and inventory
        draw_hud(self.screen, self.player, self.current_wave_index)
        self.draw_inventory()

    def check_level_up(self):
        if self.player.xp >= self.player.next_level_xp:
            self.player.level += 1
            self.player.xp -= self.player.next_level_xp
            self.player.next_level_xp *= 1.25
            level_up(self.screen, self.player, self.clock)

    def spawn_enemies(self):
        wave = ENEMY_WAVES[self.current_wave_index]
        if random.random() < 0.01 * wave.get("multi", 1):
            spawn_side = random.choice(["top", "bottom", "left", "right"])
            if spawn_side == "top":
                x = random.randint(0, WIDTH)
                y = -20
            elif spawn_side == "bottom":
                x = random.randint(0, WIDTH)
                y = HEIGHT + 20
            elif spawn_side == "left":
                x = -20
                y = random.randint(0, HEIGHT)
            elif spawn_side == "right":
                x = WIDTH + 20
                y = random.randint(0, HEIGHT)
            image = random.choice(self.enemy_images)
            speed = random.uniform(1.5, 2.5)
            self.enemies.append(Enemy(x, y, wave["hp"], wave["damage"], image, wave["xp"], wave["max_hp"], speed=speed))

    def update_wave(self):
        wave = ENEMY_WAVES[self.current_wave_index]
        elapsed_time = (pygame.time.get_ticks() - self.wave_start_time) / 1000
        if elapsed_time > wave["duration"]:
            if self.current_wave_index < len(ENEMY_WAVES) - 1:
                self.current_wave_index += 1
                self.wave_start_time = pygame.time.get_ticks()

    def check_game_over(self):
        if self.player.hp <= 0:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("Game Over!", True, RED)
            self.screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.running = False
            
    def update_items(self):
      for item in self.items[:]:
          item.draw(self.screen)
          if check_collision(self.player, item):
              item.apply_effect(self.player)
              self.items.remove(item)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.handle_events()
            self.update_player()
            self.shoot_projectiles()
            self.update_projectiles()
            self.update_enemies()
            self.update_items()
            self.spawn_enemies()
            self.update_wave()
            self.check_level_up()
            self.draw_game_elements()
            self.check_game_over()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
