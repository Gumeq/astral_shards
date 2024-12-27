import pygame
from settings import *

class UI:
    def __init__(self, font, large_font=None):
        self.font = font
        self.large_font = large_font or pygame.font.Font("assets/fonts/dogicapixel.ttf", 32)
        self.small_font = pygame.font.Font("assets/fonts/dogicapixel.ttf", 12)
        self.elapsed_pause_time = 0
        self.pause_start_time = None

    def draw_inventory(self, screen, inventory):
        slot_size = 50
        padding = 10
        
        x, y = WIDTH // 2 - 5*slot_size - 5*padding , HEIGHT - slot_size - padding*2

        for i, consumable in enumerate(inventory.consumables):
            slot_x = x + i * (slot_size + padding)
            pygame.draw.rect(screen, (50, 50, 50), (slot_x, y, slot_size, slot_size))

            if consumable:
                image_rect = consumable.image.get_rect()
                image_rect.center = (slot_x + slot_size // 2, y + slot_size // 2)
                screen.blit(consumable.image, image_rect.topleft)

                time_remaining = consumable.get_time_remaining()
                if consumable.is_active and time_remaining > 0:
                    dark_overlay = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
                    dark_overlay.fill((0, 0, 0, 150))
                    screen.blit(dark_overlay, (slot_x, y))
                    countdown_text = self.font.render(f"{int(time_remaining)}", False, (255, 255, 255))
                    text_rect = countdown_text.get_rect(center=(slot_x + slot_size // 2, y + slot_size // 2))
                    screen.blit(countdown_text, text_rect.topleft)

            pygame.draw.rect(screen, (255, 255, 255), (slot_x, y, slot_size, slot_size), 2)

    def draw_stats(self, screen, player):
        stats = [
            f"HP: {player.hp}/{player.max_hp}",
            f"Speed: {player.movement_speed:.2f}",
            f"Ability Power: {player.ability_power:.2f}",
            f"Attack Speed: {player.attack_speed:.2f}",
            f"Attack Range: {player.attack_range:.2f}",
            f"Luck: {player.luck:.2f}",
            # f"Astral Shards: {player.astral_shards}",
        ]
        x, y = 20, HEIGHT - 150
        for i, stat in enumerate(stats):
            text = self.small_font.render(stat, False, (255, 255, 255))
            screen.blit(text, (x, y + i * 20))

    def draw_shards(self, screen, player):
        shards = player.astral_shards
        x, y = WIDTH // 2 + 250 + 50 +20 , HEIGHT - 50
        text = self.font.render(f"{int(shards)}", False, (255, 255, 255))
        screen.blit(text, (x, y))

    def draw_game_time(self, screen, timer):
        total_seconds = int(timer.get_time())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_text = f"{minutes:02}:{seconds:02}"
        text_surface = self.large_font.render(time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))
        screen.blit(text_surface, text_rect)
