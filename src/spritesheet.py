import pygame

class SpriteSheet:
    def __init__(self, image_path, frame_width, frame_height):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = []
        self._split_sheet()

    def _split_sheet(self):
        """Split the sprite sheet into individual frames."""
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        for y in range(0, sheet_height, self.frame_height):
            for x in range(0, sheet_width, self.frame_width):
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                self.frames.append(frame)

    def get_frame(self, index):
        """Get a specific frame by index."""
        return self.frames[index % len(self.frames)]  # Loop around if index exceeds frame count
