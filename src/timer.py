import pygame

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

    def start(self):
        self.running = True
        self.start_time = pygame.time.get_ticks() - self.elapsed_time

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def reset(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

    def get_time(self):
        if self.running:
            return (pygame.time.get_ticks() - self.start_time) / 1000
        return self.elapsed_time / 1000
