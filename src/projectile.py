import pygame

class Projectile:
    def __init__(self, x, y, target_x, target_y, sprite_sheet, num_frames, frame_height):
        # Position and movement attributes
        self.position = pygame.math.Vector2(x, y)
        direction = pygame.math.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            direction.normalize_ip()
        self.speed = 10
        self.velocity = direction * self.speed
        self.moving = True  # Indicates if the projectile is moving

        # Animation attributes
        self.frames = self._load_frames(sprite_sheet, num_frames, frame_height)
        self.current_frame = 0
        self.animation_speed = 10  # Frames per second
        self.last_update = pygame.time.get_ticks()
        self.hit_enemy = False  # Flag to indicate collision
        self.rect = self.frames[0].get_rect(center=self.position)
        self.spawn_time = pygame.time.get_ticks()
    
    def _load_frames(self, sprite_sheet, num_frames, frame_height):
        """Extract frames from the sprite sheet."""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width = sheet_width // num_frames
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sprite_sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        return frames

    def move(self):
        if self.moving:
            self.position += self.velocity
            self.rect.center = self.position

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 // self.animation_speed:
            self.last_update = now
            self.current_frame += 1
            
            if not self.hit_enemy:
                # Before collision: Loop frames 0 to 3
                if self.current_frame > 5:
                    self.current_frame = 0
            else:
                # After collision: Continue from frame 4 onwards
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 1  # Stay on the last frame

    def draw(self, screen):
        frame = self.frames[self.current_frame]
        screen.blit(frame, self.rect.topleft)

    def is_expired(self):
        if self.hit_enemy and self.current_frame == len(self.frames) - 1:
            return True
        elif not self.hit_enemy and pygame.time.get_ticks() - self.spawn_time > 3000:
            return True
        return False
