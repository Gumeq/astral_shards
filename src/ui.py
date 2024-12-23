import pygame
from settings import *

class UI:
    def __init__(self, font , large_font=None):
        self.font = font
        self.large_font = large_font or pygame.font.Font(None, 48)  # Default to size 48 if not provided
        self.elapsed_pause_time = 0  # Total time the game was paused
        self.pause_start_time = None  # When the game was paused

    def draw_inventory(self, screen, inventory):
        """Draw the inventory with item images, overlays, and countdowns."""
        x, y = 20, 20  # Start position for inventory slots
        slot_size = 50  # Size of each inventory slot
        padding = 10    # Space between slots

        for i, consumable in enumerate(inventory.consumables):
            slot_x = x + i * (slot_size + padding)

            # Draw slot background
            pygame.draw.rect(screen, (50, 50, 50), (slot_x, y, slot_size, slot_size))

            # Draw the item image if it exists
            if consumable:
                # Center the image inside the slot
                image_rect = consumable.image.get_rect()
                image_rect.center = (slot_x + slot_size // 2, y + slot_size // 2)
                screen.blit(consumable.image, image_rect.topleft)
                # Draw countdown if the item is active
                time_remaining = consumable.get_time_remaining()
                if consumable.is_active and time_remaining > 0:
                    dark_overlay = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
                    dark_overlay.fill((0, 0, 0, 150))  # Semi-transparent black
                    screen.blit(dark_overlay, (slot_x, y))
                    # Render countdown text
                    countdown_text = self.font.render(f"{int(time_remaining)}", True, (255, 255, 255))
                    text_rect = countdown_text.get_rect(center=(slot_x + slot_size // 2, y + slot_size // 2))
                    screen.blit(countdown_text, text_rect.topleft)

            # Draw border around the slot
            pygame.draw.rect(screen, (255, 255, 255), (slot_x, y, slot_size, slot_size), 2)

    def draw_stats(self, screen, player):
        """Draw player stats."""
        stats = [
            f"HP: {player.hp}/{player.max_hp}",
            f"Speed: {player.movement_speed}",
            f"Ability Power: {player.ability_power}",
            f"Attack Speed: {player.attack_speed}",
            f"Luck: {player.luck}",
            f"Astral Shards: {player.astral_shards}",
        ]
        x, y = 20, 150
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, (255, 255, 255))
            screen.blit(text, (x, y + i * 20))
            
    def draw_shards(self, screen, player):
        shards = player.astral_shards
        x, y = (WIDTH - 40), 20
        text = self.font.render(f"{int(shards)}", True, (255, 255, 255))
        screen.blit(text, (x, y))

    def draw_game_time(self, screen, timer):
        """Draw the elapsed game time at the top center of the screen."""
        # timer.get_time() returns total unpaused seconds
        total_seconds = int(timer.get_time())

        # Format time as MM:SS
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_text = f"{minutes:02}:{seconds:02}"  # e.g. "02:35"

        # Render and position the text
        text_surface = self.large_font.render(time_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))  # top center
        screen.blit(text_surface, text_rect)
