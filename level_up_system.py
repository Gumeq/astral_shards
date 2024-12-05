# level_up_system.py
import pygame
import random
import math
from settings import WIDTH, HEIGHT, WHITE, RED

def apply_upgrade(player, upgrade):
    if upgrade["effect"] == "max_hp":
        player.max_hp += upgrade["value"]
        player.hp += upgrade["value"]
    elif upgrade["effect"] == "damage":
        player.damage += upgrade["value"]
    elif upgrade["effect"] == "fire_rate":
        player.fire_rate = max(10, player.fire_rate + upgrade["value"])
    elif upgrade["effect"] == "luck":
        player.luck += upgrade["value"]
    elif upgrade["effect"] == "special_ability":
        player.special_ability = True

def level_up(screen, player, clock):
    upgrade_options = [
        {"name": "Increase Max HP", "effect": "max_hp", "value": 25},
        {"name": "Increase Damage", "effect": "damage", "value": 25},
        {"name": "Increase Fire Rate", "effect": "fire_rate", "value": -25},
        {"name": "Increase Luck", "effect": "luck", "value": 5},
    ]
    if random.random() < 0.1 * player.luck and not player.special_ability:
        upgrade_options.append({
            "name": "Unlock Triple Shot Ability",
            "effect": "special_ability",
            "value": True
        })
    

    selected_option = 0
    selection_made = False
    level_up_start_time = pygame.time.get_ticks()

    while not selection_made:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(upgrade_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(upgrade_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    apply_upgrade(player, upgrade_options[selected_option])
                    selection_made = True
        elapsed_time = (pygame.time.get_ticks() - level_up_start_time) / 1000
        if elapsed_time >= 30:
            apply_upgrade(player, upgrade_options[0])
            selection_made = True
        font = pygame.font.Font(None, 36)
        title_text = font.render("Level Up! Choose an Upgrade:", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        for i, option in enumerate(upgrade_options):
            color = RED if i == selected_option else WHITE
            option_text = font.render(option["name"], True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 200 + i * 40))
        timer_text = font.render(f"Time remaining: {int(30 - elapsed_time)} seconds", True, WHITE)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 400))
        pygame.display.flip()
        clock.tick(60)
