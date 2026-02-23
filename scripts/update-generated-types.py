"""Generate types based on Discord API."""

from pathlib import Path

import discord

import discord_guild_configurator.generated_models

generated_file = Path(discord_guild_configurator.generated_models.__file__)


permission_options: list[str] = sorted(discord.Permissions.VALID_FLAGS)

lines = [
    "from typing import Literal",
    "",
    "Permission = Literal[",
    *(f'    "{option}",' for option in permission_options),
    "]",
    "",
]

generated_file.write_text("\n".join(lines), encoding="UTF-8", newline="\n")
