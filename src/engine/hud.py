import pygame
from src.config.settings import FONT_INTERFACE, FONT_SIZE


class Hud:
    def __init__(self, parent):
        self.parent = parent
        self.font_interface = pygame.font.SysFont(FONT_INTERFACE, FONT_SIZE)

    def draw_player_var(self, surface, player):
        if player is None:
            return

        color_ammo = (200, 0, 0) if player.player_bullets <= 0 else (50, 50, 50)
        ammo_text = self.font_interface.render(f"Ammo: {player.player_bullets}", True, color_ammo)
        surface.blit(ammo_text, (20, 40))


        pygame.draw.rect(surface, (200, 200, 200), (95, 22, 150, 20), border_radius=10)

        life_width = (player.health / player.stats.hlt) * 150
        pygame.draw.rect(surface, (255, 0, 0), (95, 22, life_width, 20), border_radius=10)

        health_text = self.font_interface.render("Health: ", True, (50, 50, 50))
        surface.blit(health_text, (20, 20))