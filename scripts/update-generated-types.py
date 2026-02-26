"""Generate types based on Discord API."""

from collections import defaultdict
from pathlib import Path

import discord
from attr import dataclass

import discord_guild_configurator

generated_file = Path(discord_guild_configurator.__file__).parent / "generated_models.py"


@dataclass(frozen=True)
class CodegenOutput:
    imports: dict[str, list[str]]
    code_lines: list[str]


def generate_flag_lines(flags_cls: type[discord.flags.BaseFlags]) -> CodegenOutput:
    return CodegenOutput(
        imports={"typing": ["Literal"]},
        code_lines=[
            f"{flags_cls.__name__} = Literal[",
            *(f'    "{option}",' for option in sorted(flags_cls.VALID_FLAGS)),
            "]",
        ],
    )


def generate_enum_lines(enum_cls: type[discord.Enum]) -> CodegenOutput:
    return CodegenOutput(
        imports={"typing": ["Literal"]},
        code_lines=[
            f"{enum_cls.__name__} = Literal[",
            *(f'    "{option.name}",' for option in sorted(enum_cls)),
            "]",
        ],
    )


def generate_lines(outputs: list[CodegenOutput]) -> list[str]:
    imports: dict[str, set[str]] = defaultdict(set)
    code_lines = []
    for output in outputs:
        for import_module, import_names in output.imports.items():
            imports[import_module].update(import_names)

        code_lines.extend(output.code_lines)

    lines: list[str] = []
    for import_module, import_names in sorted(imports.items()):
        lines.append(f"from {import_module} import {', '.join(sorted(import_names))}")
    lines.append("")
    lines.extend(code_lines)
    lines.append("")
    return lines


outputs = [
    generate_flag_lines(discord.Permissions),
    generate_enum_lines(discord.VerificationLevel),
    generate_enum_lines(discord.NotificationLevel),
    generate_enum_lines(discord.Locale),
    generate_enum_lines(discord.ContentFilter),
]

generated_file.write_text("\n".join(generate_lines(outputs)), encoding="UTF-8", newline="\n")
