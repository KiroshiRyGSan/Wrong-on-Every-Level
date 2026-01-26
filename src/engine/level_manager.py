import pygame
import pytmx
from pathlib import Path
from src.config.level_dtclass import LevelConfig

TMX_BASE_PATH = Path(__file__).parent.parent / "assets" / "data" / "maps"


class Level:
    def __init__(self, level_config: LevelConfig) -> None:
        self.config: LevelConfig = level_config

        tmx_path = TMX_BASE_PATH / self.config.tmx_file

        if not tmx_path.exists():
            raise FileNotFoundError(f"TMX file not found: {tmx_path}")

        self.tmx_data = pytmx.load_pygame(str(tmx_path), pixelalpha=True)

        self.collision_rects = []
        self.map_surface = self._pre_render_map()
        self._build_collisions()

    def _pre_render_map(self):
        width = self.tmx_data.width * self.tmx_data.tilewidth
        height = self.tmx_data.height * self.tmx_data.tileheight
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))
        return surface

    def _build_collisions(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props and props.get("solid"):
                        rect = pygame.Rect(
                            x * self.tmx_data.tilewidth,
                            y * self.tmx_data.tileheight,
                            self.tmx_data.tilewidth,
                            self.tmx_data.tileheight
                        )
                        self.collision_rects.append(rect)

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.map_surface, offset)


