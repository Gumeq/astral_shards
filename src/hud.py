import pygame
from settings import RED, GREEN, WHITE

def draw_hud(screen, player, wave_index):
    # Font for text
    font = pygame.font.Font(None, 36)

    # Text for HP
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)
    screen.blit(hp_text, (20, 20))

    # Damage
    damage_text = font.render(f"Damage: {player.damage}", True, WHITE)
    screen.blit(damage_text, (20, 60))

    # Fire Rate
    fire_rate_text = font.render(f"Fire Rate: {60 / (player.fire_rate / 1000):.2f} shots/sec", True, WHITE)
    screen.blit(fire_rate_text, (20, 100))

    # Experience
    xp_text = font.render(f"XP: {player.xp}", True, WHITE)
    screen.blit(xp_text, (20, 140))

    # Current Wave
    wave_text = font.render(f"Wave: {wave_index + 1}", True, WHITE)
    screen.blit(wave_text, (20, 180))
