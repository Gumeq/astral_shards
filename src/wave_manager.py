import pygame
import json
import random
from src.enemy import Enemy  # Assumes you have an Enemy class

class WaveManager:
    def __init__(self, wave_file, world, enemy_data, enemy_manager, camera, timer):
        """
        Initialize the Wave Manager.
        :param wave_file: Path to the JSON file containing wave data.
        :param world: The World instance to spawn enemies into.
        :param enemy_data: Enemy data loaded from an enemy JSON file.
        """
        self.wave_file = wave_file
        self.world = world
        self.camera = camera
        self.enemy_data = enemy_data  # Reference to enemy properties
        self.current_wave = None
        self.waves = self.load_waves(self.wave_file)
        self.wave_index = 0
        self.start_time = None
        self.enemies_spawned = 0
        self.enemy_manager = enemy_manager
        
        
        self.timer = timer

    def load_waves(self, wave_file):
        """Load wave configurations from a JSON file."""
        with open(wave_file, "r") as f:
            return json.load(f)

    def start_wave(self, wave_index):
        """Start a new wave."""
        self.wave_index = wave_index
        if wave_index < len(self.waves):
            self.current_wave = self.waves[wave_index]
            # wave_start_offset = total game time so far
            self.wave_start_offset = self.timer.get_time()
            self.enemies_spawned = 0
            print(f"Wave {self.current_wave['wave_number']} started.")
        else:
            self.current_wave = None
            print("No more waves.")


    def reset(self):
        """
        Reset everything needed to start from the first wave again.
        """
        self.waves = self.load_waves(self.wave_file)
        self.wave_index = 0
        self.current_wave = None
        self.enemies_spawned = 0
        self.start_time = None
        self.wave_start_offset = 0

        # Optionally start the first wave right away,
        # or let the game call start_wave(0) when gameplay begins
        # self.start_wave(0

    def update(self):
        if not self.current_wave:
            return

        # total game time so far
        current_game_time = self.timer.get_time()

        # how many seconds have passed *since the wave started*
        elapsed_time = current_game_time - self.wave_start_offset

        # End the wave if its duration has elapsed
        if elapsed_time >= self.current_wave["duration"]:
            self.end_wave()
            return

        # Spawn enemies based on spawn rate
        spawn_interval = 1 / self.current_wave["spawn_rate"]

        # The condition: self.enemies_spawned * spawn_interval <= elapsed_time
        # means "can I spawn the next enemy?"
        while self.enemies_spawned * spawn_interval <= elapsed_time:
            self.spawn_enemy()
            self.enemies_spawned += 1

    def spawn_enemy(self):
        """Spawn an enemy just outside the camera view based on the current wave configuration."""
        for enemy_group in self.current_wave["enemies"]:
            if enemy_group["count"] > 0:
                enemy_type = enemy_group["type"]
                if enemy_type in self.enemy_data:
                    enemy_properties = self.enemy_data[enemy_type]

                    # Get the camera's offset
                    camera_offset = self.camera.offset

                    # Define spawn zones
                    spawn_zone = random.choice(["top", "bottom", "left", "right"])
                    if spawn_zone == "top":
                        x = random.randint(int(camera_offset.x), int(camera_offset.x + self.camera.screen_width))
                        y = int(camera_offset.y - 50)  # Just above the top edge
                    elif spawn_zone == "bottom":
                        x = random.randint(int(camera_offset.x), int(camera_offset.x + self.camera.screen_width))
                        y = int(camera_offset.y + self.camera.screen_height + 50)  # Just below the bottom edge
                    elif spawn_zone == "left":
                        x = int(camera_offset.x - 50)  # Just to the left of the screen
                        y = random.randint(int(camera_offset.y), int(camera_offset.y + self.camera.screen_height))
                    elif spawn_zone == "right":
                        x = int(camera_offset.x + self.camera.screen_width + 50)  # Just to the right of the screen
                        y = random.randint(int(camera_offset.y), int(camera_offset.y + self.camera.screen_height))

                    # Clamp to world boundaries (optional, depending on your world logic)
                    x = max(0, min(x, self.world.width))
                    y = max(0, min(y, self.world.height))

                    # Spawn the enemy
                    enemy = Enemy(x, y, enemy_properties, self.world)
                    self.enemy_manager.enemies.append(enemy)
                    enemy_group["count"] -= 1
                    print(f"Spawned {enemy_type} at ({x}, {y}).")
                    return  # Spawn one enemy at a time

    def end_wave(self):
        """End the current wave and prepare for the next one."""
        print(f"Wave {self.current_wave['wave_number']} ended.")
        self.current_wave = None
        self.start_wave(self.wave_index + 1)
