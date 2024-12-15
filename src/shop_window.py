import pygame
import json
import logging
from settings import *

class Shop:
    def __init__(self, font, player, consumable_manager, shop_data_file):
        self.font = font
        self.player = player
        self.consumable_manager = consumable_manager
        self.visible = False
        self.selected_index = 0
        self.items = self.load_shop_items(shop_data_file)

        # Separate items into categories
        self.buff_items = [item for item in self.items if item["type"] == "buff"]
        self.consumable_items = [item for item in self.items if item["type"] == "consumable"]

        # Larger fonts for title and section headers
        self.title_font = pygame.font.Font(None, 36)  # Larger font for title
        self.header_font = pygame.font.Font(None, 28) # Font for section headers

    def load_shop_items(self, shop_data_file):
        """Load shop items from a JSON file."""
        with open(shop_data_file, "r") as f:
            data = json.load(f)
        return data["items"]

    def toggle(self):
        """Open/close the shop."""
        self.visible = not self.visible
        if self.visible:
            self.selected_index = 0  # Reset selection when opened

    def handle_input(self, event):
        """Handle keyboard input when the shop is open."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % (len(self.buff_items) + len(self.consumable_items))
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % (len(self.buff_items) + len(self.consumable_items))
            elif event.key == pygame.K_RETURN:
                all_items = self.buff_items + self.consumable_items
                self.buy_item(all_items[self.selected_index])
            elif event.key == pygame.K_ESCAPE:
                self.toggle()

    def buy_item(self, item):
        """Attempt to purchase the selected item."""
        cost = item["cost"]
        if self.player.astral_shards >= cost:
            # Check if it's a consumable and if there's space
            if item["type"] == "consumable":
                if not self.player.inventory.has_consumable_space():
                    logging.info("No space in inventory for this consumable. Purchase cancelled.")
                    return
            self.player.astral_shards -= cost
            if item["type"] == "buff":
                self.apply_buff(item)
            elif item["type"] == "consumable":
                self.add_consumable(item)
            logging.info(f"Player purchased {item['name']} for {cost} shards.")
        else:
            logging.info("Not enough Astral Shards to purchase item.")

    def apply_buff(self, item):
        """Apply a buff directly to the player."""
        effect = item["effect"]
        magnitude = item["magnitude"]
        duration = item.get("duration", 0)
        if effect == "max_hp":
            self.player.max_hp += magnitude
            self.player.hp = self.player.max_hp
        else:
            if duration == 0:
                # Permanent buff
                if effect == "movement_speed":
                    self.player.movement_speed += magnitude
                elif effect == "ability_power":
                    self.player.ability_power += magnitude
                elif effect == "attack_speed": 
                    self.player.attack_speed *= magnitude
                elif effect == "attack_range": 
                    self.player.attack_range *= magnitude
                elif effect == "luck":
                    self.player.luck += magnitude
            else:
                # Timed buff if you want to implement
                self.player.add_buff(effect, magnitude, duration)

    def add_consumable(self, item):
        """Add a consumable to the player's inventory if there's space."""
        consumable = self.consumable_manager.create_consumable(item["consumable_name"])
        if consumable:
            self.player.inventory.add_consumable(consumable)
            logging.info(f"Added {consumable.name} to inventory.")
        else:
            logging.warning(f"Consumable '{item['consumable_name']}' not found.")

    def draw(self, screen):
        """Draw the shop UI with improved visuals."""
        if not self.visible:
            return

        # Dark overlay (semi-transparent)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0))

        shop_width, shop_height = 500, 700
        shop_rect = pygame.Rect(
            (WIDTH - shop_width) // 2,
            (HEIGHT - shop_height) // 2,
            shop_width,
            shop_height
        )
        pygame.draw.rect(screen, (50, 50, 50), shop_rect)
        pygame.draw.rect(screen, (255, 255, 255), shop_rect, 2)

        # Display Player Shards at top right inside the shop
        shards_text = f"{self.player.astral_shards} sh"
        shards_surface = self.font.render(shards_text, True, (255, 255, 255))
        shards_rect = shards_surface.get_rect(topright=(shop_rect.right - 10, shop_rect.top + 10))
        screen.blit(shards_surface, shards_rect.topleft)

        # Title
        title_text = self.title_font.render("Shop", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(shop_rect.centerx, shop_rect.y + 30))
        screen.blit(title_text, title_rect.topleft)

        # Draw section headers: Buffs and Consumables
        y_start = title_rect.bottom + 20
        # Buff section
        buff_header = self.header_font.render("Buffs", True, (0, 150, 255))  # Blue for buffs
        buff_header_rect = buff_header.get_rect(x=shop_rect.x + 20, y=y_start)
        screen.blit(buff_header, buff_header_rect.topleft)
        y_offset = buff_header_rect.bottom + 10

        # Items per section
        line_height = 40
        all_items = self.buff_items + self.consumable_items
        total_buffs = len(self.buff_items)

        # Draw Buff Items
        for i, item in enumerate(self.buff_items):
            idx = i  # i is index within buffs
            selected = (idx == self.selected_index)
            self.draw_item_line(screen, item, shop_rect, y_offset + i * line_height, selected, is_buff=True)

        # Consumable section
        y_offset += len(self.buff_items)*line_height + 20
        consumable_header = self.header_font.render("Consumables", True, (0, 255, 0))  # Green for consumables
        consumable_header_rect = consumable_header.get_rect(x=shop_rect.x + 20, y=y_offset)
        screen.blit(consumable_header, consumable_header_rect.topleft)
        y_offset = consumable_header_rect.bottom + 10

        # Draw Consumable Items
        for j, item in enumerate(self.consumable_items):
            idx = total_buffs + j
            selected = (idx == self.selected_index)
            self.draw_item_line(screen, item, shop_rect, y_offset + j * line_height, selected, is_buff=False)

        # Draw selected item details at bottom panel
        detail_height = 60
        detail_rect = pygame.Rect(shop_rect.x + 10, shop_rect.bottom - detail_height - 10, shop_width - 20, detail_height)
        pygame.draw.rect(screen, (40, 40, 40), detail_rect)
        pygame.draw.rect(screen, (255,255,255), detail_rect, 1)

        if 0 <= self.selected_index < len(all_items):
            selected_item = all_items[self.selected_index]
            self.draw_item_details(screen, selected_item, detail_rect)

    def draw_item_line(self, screen, item, shop_rect, y_pos, selected, is_buff):
        """Draw a single item line in the shop list."""
        x_start = shop_rect.x + 20
        # Add an arrow if selected
        arrow = "→ " if selected else "  "

        # Base text: Name and Cost
        base_text = f"{arrow}{item['name']} - {item['cost']} sh"

        # If it's a buff, show effect text
        if is_buff:
            effect_text = f"+{item['magnitude']} {item['effect'].replace('_',' ').capitalize()}"
            item_text = base_text + " | " + effect_text
        else:
            # Consumable - show just base_text, details will show in panel
            item_text = base_text

        color = (255, 255, 255)
        item_surface = self.font.render(item_text, True, color)
        screen.blit(item_surface, (x_start, y_pos))

    def draw_item_details(self, screen, item, detail_rect):
        """Show more info about the selected item in the bottom panel."""
        # For buffs: Show what it does, permanent or not
        # For consumables: Show image and a brief description
        x_start = detail_rect.x + 10
        y_start = detail_rect.y + 10

        if item["type"] == "buff":
            # Show details: Name, effect, magnitude
            name_surface = self.font.render(item["name"], True, (255, 255, 255))
            screen.blit(name_surface, (x_start, y_start))

            effect_str = f"Increases your {item['effect'].replace('_',' ')} by {item['magnitude']} permanently."
            effect_surface = self.font.render(effect_str, True, (200, 200, 200))
            screen.blit(effect_surface, (x_start, y_start + 20))
        else:
            # Consumable
            consumable = self.consumable_manager.create_consumable(item["consumable_name"])
            name_surface = self.font.render(item["name"], True, (255, 255, 255))
            screen.blit(name_surface, (x_start, y_start))

            if consumable and consumable.image:
                # Draw image on left side of detail panel
                image_rect = consumable.image.get_rect()
                # Scale if too large
                max_dim = 16
                if image_rect.width > max_dim or image_rect.height > max_dim:
                    scale_factor = max_dim / max(image_rect.width, image_rect.height)
                    new_w = int(image_rect.width * scale_factor)
                    new_h = int(image_rect.height * scale_factor)
                    image = pygame.transform.scale(consumable.image, (new_w, new_h))
                else:
                    image = consumable.image

                img_y = y_start + 25
                image_rect = image.get_rect(topleft=(x_start, img_y))
                screen.blit(image, image_rect.topleft)

                text_x = x_start + image_rect.width + 10
                desc_str = f"{consumable.name}: {consumable.effect.capitalize()} +{consumable.magnitude}"
                desc_surface = self.font.render(desc_str, True, (200,200,200))
                screen.blit(desc_surface, (text_x, img_y))
            else:
                # No image, just text
                no_image_text = "A special consumable item."
                no_img_surface = self.font.render(no_image_text, True, (200,200,200))
                screen.blit(no_img_surface, (x_start, y_start + 20))
