import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    token: str
    free_games_channel_id: int | None


def load_config() -> Config:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN fehlt in der .env")

    channel_id = os.getenv("FREE_GAMES_CHANNEL_ID")
    return Config(
        token=token, free_games_channel_id=int(channel_id) if channel_id else None
    )
