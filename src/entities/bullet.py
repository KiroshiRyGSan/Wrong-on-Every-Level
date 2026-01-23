import pygame
import math
from src.core.h_assets_loader import AssetsLoader
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from typing import List, Tuple, Dict

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target: Tuple[int, int], difficulty: str, character: str):
        super().__init__()
        self.animation: List[pygame.Surface] = AssetsLoader.load_bullet_images("player", difficulty, character)
        self.frame_index = 0
        self.animation_speed = 0.07
        delta_x = target[0] - start_pos[0]
        delta_y = target[1] - start_pos[1]
        self.angle = math.atan2(delta_y, delta_x)

        self.speed = 10
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed

        image_to_rotate = self.animation[self.frame_index]
        self.image = pygame.transform.rotate(image_to_rotate, -math.degrees(self.angle))

        self.rect = self.image.get_rect(center=start_pos)
        self.damage = 1

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        rotated_image = self.animation[int(self.frame_index)]
        self.image = pygame.transform.rotate(rotated_image, -math.degrees(self.angle))
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.animate()

        margin = 100
        if (self.rect.right < -margin or self.rect.left > SCREEN_WIDTH + margin or
                self.rect.bottom < -margin or self.rect.top > SCREEN_HEIGHT + margin):
            self.kill()
