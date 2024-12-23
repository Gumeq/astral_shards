import pygame

def load_projectile_sprite():
    sprite_sheet = pygame.image.load("assets/images/player/Charge.png").convert_alpha()
    return sprite_sheet

def load_player_animations():
    animations = {}
    animation_data = {
        "Idle": {
            "path": "assets/images/player/Idle.png",
            "num_frames": 7,
            "frame_height": 128
        },
        "Run": {
            "path": "assets/images/player/Run.png",
            "num_frames": 8,
            "frame_height": 128
        },
        "Attack": {
            "path": "assets/images/player/Fireball.png",
            "num_frames": 8,
            "frame_height": 128
        },
        "Hurt": {
            "path": "assets/images/player/Hurt.png",
            "num_frames": 3,
            "frame_height": 128
        },
        "Dead": {
            "path": "assets/images/player/Dead.png",
            "num_frames": 6,
            "frame_height": 128
        }
    }

    for animation_name, data in animation_data.items():
        sprite_sheet = pygame.image.load(data["path"]).convert_alpha()
        frames = _load_frames(sprite_sheet, data["num_frames"], data["frame_height"])
        animations[animation_name] = frames
    return animations

def _load_frames(sprite_sheet, num_frames, frame_height):
    """Extract frames from the sprite sheet."""
    frames = []
    sheet_width, _ = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sprite_sheet.subsurface(frame_rect).copy()
        frames.append(frame)
    return frames
