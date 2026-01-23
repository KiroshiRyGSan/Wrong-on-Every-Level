import pygame
from pathlib import Path
from typing import Dict, List

BASE_PATH: Path = Path(__file__).parent.parent / "assets" / "images"


def load_image(path: Path) -> pygame.Surface:
    full_path = BASE_PATH / path
    return pygame.image.load(str(full_path)).convert_alpha()

def load_animation_frames(folder_path: Path) -> List[pygame.Surface]:
    frames = sorted(folder_path.glob("frame_*.png"))
    return [load_image(frame.relative_to(BASE_PATH)) for frame in frames]

class AssetsLoader:
    @staticmethod
    def load_player_images(type: str, difficulty: str, character: str) -> Dict[str, List[pygame.Surface]]:
        base = BASE_PATH / type / difficulty / character

        animations = {}

        for anim_folder in base.iterdir():
            if anim_folder.is_dir():
                animations[anim_folder.name] = load_animation_frames(anim_folder)

        return animations


    @staticmethod
    def load_bullet_images(type: str, difficulty: str, character: str) -> List[pygame.Surface]:
        base = BASE_PATH / type / difficulty / character / "bullets"

        if base.exists():
            return load_animation_frames(base)

        return []