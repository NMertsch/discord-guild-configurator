# ruff: noqa: F541
"""Generate types based on Discord API."""

from pathlib import Path

import discord

import discord_guild_configurator

generated_file = Path(discord_guild_configurator.__file__).parent / "generated_models.py"


def generate_flag_lines(flags_cls: type[discord.flags.BaseFlags]) -> list[str]:
    return [
        f"{flags_cls.__name__} = Literal[",
        *(f'    "{option}",' for option in sorted(flags_cls.VALID_FLAGS)),
        "]",
    ]


def generate_enum_annotated_lines(enum_cls: type[discord.Enum]) -> list[str]:
    name = enum_cls.__name__
    return [
        f"{name} = Annotated[",
        f"    discord.{name},",
        f"    pydantic.PlainValidator(",
        f"        lambda value: discord.{name}[value] if isinstance(value, str) else value",
        f"    ),",
        f"    pydantic.PlainSerializer(lambda value: value.name),",
        f"    pydantic.Field(",
        f"        json_schema_extra={{",
        f'            "enum": [option.name for option in discord.{name}],',
        f'            "type": "string",',
        f"        }},",
        f"    ),",
        f"]",
    ]


lines: list[str] = [
    "from typing import Annotated, Literal",
    "",
    "import discord",
    "import pydantic",
    "",
    *generate_flag_lines(discord.Permissions),
    *generate_enum_annotated_lines(discord.VerificationLevel),
    *generate_enum_annotated_lines(discord.NotificationLevel),
    *generate_enum_annotated_lines(discord.Locale),
    *generate_enum_annotated_lines(discord.ContentFilter),
    "",
]

generated_file.write_text("\n".join(lines), encoding="UTF-8", newline="\n")
