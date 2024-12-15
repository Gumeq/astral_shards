import pygame
def load_enemy_images():
    images = [
        pygame.image.load("assets/images/enemies/Icon2.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon3.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon4.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon5.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon6.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon7.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon8.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon9.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon10.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon11.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon12.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon13.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon14.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon15.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon16.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon17.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon18.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon19.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon20.png").convert_alpha(),
        pygame.image.load("assets/images/enemies/Icon21.png").convert_alpha(),
    ]
    images = [pygame.transform.scale(img, (100, 100)) for img in images]
    return images

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
