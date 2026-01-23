import pygame
from src.entities.player import Player
from src.engine.screen import Screen
from src.engine.hud import Hud
from src.core.settings import *


def main():
    pygame.init()

    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    hud = Hud(None)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    player = Player(100, 500, "easy", "priest", 0, 780)
    all_sprites.add(player)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in secondi

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(bullet_group)
        bullet_group.update()

        for bullet in bullet_group:
            if bullet not in all_sprites:
                all_sprites.add(bullet)

        screen.fill(BLACK)
        all_sprites.draw(screen.display)
        hud.draw_player_var(screen.display, player)
        screen.update()

    pygame.quit()


if __name__ == "__main__":
    main()