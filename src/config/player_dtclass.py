from dataclasses import dataclass
import json
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent.parent /"src" / "assets" / "data" / "player.json"

@dataclass(frozen=True)
class PlayerConfig:
    dmg: int
    hlt: int
    blts: int
    rld_time_ms: int
    vel: int=10


def load_player_stats(difficulty: str, character: str) -> PlayerConfig:
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Path not found: {JSON_PATH}")

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    try:
        stats_data = data[difficulty][character]
        return PlayerConfig(**stats_data)
    except KeyError:
        raise ValueError(f"Configurazione non valida per {difficulty} -> {character}")
