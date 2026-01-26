from dataclasses import dataclass
from pathlib import Path
import json
from typing import Optional

JSON_PATH = Path(__file__).parent.parent / "assets" / "data" / "levels.json"

@dataclass(frozen=True)
class LevelConfig:
    name: str
    tmx_file: str
    spawn_point: list[int]
    bg_music: Optional[str] = None


def load_level_config(level_id: str) -> LevelConfig:
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"JSON doesn't exist: {JSON_PATH}")

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    if level_id not in data:
        raise ValueError(f"Level'{level_id}' not found in JSON")

    return LevelConfig(**data[level_id])