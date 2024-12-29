import pygame
import json
import random
from src.enemy import Enemy, Demon

class WaveManager:
    def __init__(self, wave_file, world, enemy_data, enemy_manager, camera, timer):
        self.wave_file = wave_file
        self.world = world
        self.camera = camera
        self.enemy_data = enemy_data
        self.enemy_manager = enemy_manager
        self.timer = timer
        self.waves = self.load_waves(wave_file)
        self.current_wave = None
        self.wave_index = 0
        self.enemies_spawned = 0
        self.wave_start_offset = 0

    def load_waves(self, wave_file):
        with open(wave_file, "r") as f:
            return json.load(f)

    def start_wave(self, wave_index):
        self.wave_index = wave_index
        if wave_index < len(self.waves):
            self.current_wave = self.waves[wave_index]
            self.wave_start_offset = self.timer.get_time()
            self.enemies_spawned = 0
            print(f"Wave {self.current_wave['wave_number']} started.")
        else:
            self.current_wave = None
            print("No more waves.")

    def reset(self):
        self.waves = self.load_waves(self.wave_file)
        self.wave_index = 0
        self.current_wave = None
        self.enemies_spawned = 0
        self.wave_start_offset = 0

    def update(self):
        """Updates the status of the wave, spawns enemies if needed, 
        and checks if conditions are met to move to the next wave."""
        if not self.current_wave:
            return

        current_game_time = self.timer.get_time()
        elapsed_time = current_game_time - self.wave_start_offset

        # 1. Check if the wave duration has ended
        if elapsed_time >= self.current_wave["duration"]:
            self.end_wave()
            return

        # 2. Check if all enemies are spawned AND there are no enemies alive
        if all(enemy_group["count"] <= 0 for enemy_group in self.current_wave["enemies"]) and len(self.world.enemies) == 0:
            self.end_wave()
            return

        # Calculate spawn interval based on the spawn_rate
        spawn_interval = 1 / self.current_wave["spawn_rate"]

        # Spawn enemies while the required time interval has passed
        while self.enemies_spawned * spawn_interval <= elapsed_time:
            self.spawn_enemy()
            self.enemies_spawned += 1

    def spawn_enemy(self):
        """Spawns one enemy if there's any left to spawn in the wave."""
        for enemy_group in self.current_wave["enemies"]:
            if enemy_group["count"] > 0:
                enemy_type = enemy_group["type"]
                if enemy_type in self.enemy_data:
                    enemy_properties = self.enemy_data[enemy_type]
                    camera_offset = self.camera.offset
                    spawn_zone = random.choice(["top", "bottom", "left", "right"])

                    if spawn_zone == "top":
                        x = random.randint(int(camera_offset.x),
                                           int(camera_offset.x + self.camera.screen_width))
                        y = int(camera_offset.y - 50)
                    elif spawn_zone == "bottom":
                        x = random.randint(int(camera_offset.x),
                                           int(camera_offset.x + self.camera.screen_width))
                        y = int(camera_offset.y + self.camera.screen_height + 50)
                    elif spawn_zone == "left":
                        x = int(camera_offset.x - 50)
                        y = random.randint(int(camera_offset.y),
                                           int(camera_offset.y + self.camera.screen_height))
                    else:  # "right"
                        x = int(camera_offset.x + self.camera.screen_width + 50)
                        y = random.randint(int(camera_offset.y),
                                           int(camera_offset.y + self.camera.screen_height))

                    # Clamp positions to world boundaries
                    x = max(0, min(x, self.world.width))
                    y = max(0, min(y, self.world.height))

                    # Create the appropriate enemy subclass
                    if enemy_type == "demon" or enemy_type == "magma_demon" or enemy_type == "lunar_mage" or enemy_type == "magma_demon":
                        enemy = Demon(x, y, enemy_properties, self.world)
                    else:
                        enemy = Enemy(x, y, enemy_properties, self.world)

                    self.world.enemies.append(enemy)
                    enemy_group["count"] -= 1
                    print(f"Spawned {enemy_type} at ({x}, {y}).")
                    return

    def end_wave(self):
        """Ends the current wave and starts the next wave."""
        print(f"Wave {self.current_wave['wave_number']} ended.")
        self.current_wave = None
        self.start_wave(self.wave_index + 1)
