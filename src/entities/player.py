import pygame
from src.config.player_dtclass import PlayerConfig, load_player_stats
from src.core.h_assets_loader import AssetsLoader
from typing import Dict, List
from src.entities.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, difficulty: str, character: str, min_level_border: int, max_level_border: int):
        super().__init__()

        self.stats: PlayerConfig = load_player_stats(difficulty, character)
        self.animations: Dict[str, List[pygame.Surface]] = AssetsLoader.load_player_images(
            "player", difficulty, character
        )

        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.07
        self.player_facing_left = False
        self.gravity = 0
        self.shoot_cooldown = 500
        self.last_shot = 0
        self.player_y = y
        self.max_level_border_y = max_level_border
        self.min_level_border_y = min_level_border
        self.player_bullets = self.stats.blts
        self.move_velocity = self.stats.vel
        self.health = self.stats.hlt

        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, bullet_group):
        self.get_status()
        self.animate()
        self.move()
        self.jump()
        self.update_gravity()
        self.ammo_handler()
        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_s]:
            if self.player_bullets > 0:
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_cooldown:
                    mouse_pos = pygame.mouse.get_pos()
                    self.shoot(self.rect.center, mouse_pos[0], mouse_pos[1], bullet_group)


    def get_status(self):
        if self.status == 'shoot':
            if self.frame_index < len(self.animations['shoot']) - 1:
                return

        keys = pygame.key.get_pressed()

        if self.rect.bottom < self.player_y:
            self.status = 'jump'

        elif keys[pygame.K_a] and self.rect.left > 10:
            self.status = 'run'

        elif keys[pygame.K_d]:
            self.status = 'run'

        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = pygame.transform.flip(image, self.player_facing_left, False)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_a] and self.rect.left > self.min_level_border_y:
            self.player_facing_left = True
            self.rect.left -= self.move_velocity
        elif pygame.key.get_pressed()[pygame.K_d] and self.rect.right < self.max_level_border_y:
            self.player_facing_left = False
            self.rect.left += self.move_velocity

    def jump(self):
        if pygame.key.get_pressed()[pygame.K_w] and self.rect.bottom >= self.player_y:
            self.gravity -= 28
            if self.rect.bottom == self.player_y:
                self.frame_index = 0

    def update_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= self.player_y:
            self.gravity = 0
            self.rect.bottom = self.player_y

    def ammo_handler(self):
        if self.player_bullets > 0:
            return True
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.stats.rld_time_ms:
            self.player_bullets = self.stats.blts
            print("Ricarica completata!")
            return True
        else:
            return False


    def shoot(self, start, target_x, target_y, bullet_group):
        self.player_bullets -= 1
        self.last_shot = pygame.time.get_ticks()
        self.status = 'shoot'
        self.frame_index = 0
        bullet = Bullet(start, (target_x, target_y), "easy", "priest")
        bullet_group.add(bullet)