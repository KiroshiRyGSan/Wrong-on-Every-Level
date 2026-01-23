import pygame

class Screen:
    def __init__(self, width: int, height: int, title: str):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def fill(self, color):
        self.display.fill(color)

    def update(self):
        pygame.display.flip()