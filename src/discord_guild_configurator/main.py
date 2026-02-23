from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from discord_guild_configurator.bot import GuildConfigurationBot, run_bot
from discord_guild_configurator.configurator import GuildConfigurator
from discord_guild_configurator.models import GuildConfig

if TYPE_CHECKING:
    import discord

DESCRIPTION = """\
Configure a Discord guild.

Requires the environment variable 'BOT_TOKEN' to be set.
Requires bot privileges for receiving 'GUILD_MEMBER' events.

It will:
- Enable 'Community Server' features
- Configure system channels
- Update roles
    - Add missing roles
    - Update colors
    - Update 'hoist' flag
    - Update 'mentionable' flag
    - Update role permissions
- Update categories, text channels, and forums
    - Add missing categories, text channels, and forums
    - Update positions
    - Add missing forum tags
    - Update 'mandatory/optional' state of forum tags
    - Update category, text channel, and forum permission overwrites
- Update category and channel permission overwrites
- Update channel's default messages

To do manually:
- Configure role order

It will not:
- Delete roles
- Delete categories
- Delete channels
- Delete forum tags
- Delete human-authored messages

All operations are idempotent. Applying the same configuration twice will perform no changes.
"""


def configure_logging(*, verbose: bool = False, debug: bool = False) -> None:
    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    log_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler.addFilter(
        # silence irrelevant warning
        lambda record: record.msg != "PyNaCl is not installed, voice will NOT be supported"
    )
    logging.basicConfig(level=log_level, handlers=[log_handler])


def main() -> None:
    """Run this application."""
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--guild-id", type=int, required=True, help="ID of the guild to configure")
    parser.add_argument(
        "--config-file",
        type=Path,
        required=True,
        help="Path to the guild configuration file (JSON)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable INFO logging")
    parser.add_argument("--debug", action="store_true", help="Enable DEBUG logging")
    args = parser.parse_args()

    bot_token = os.getenv("BOT_TOKEN")
    if bot_token is None:
        raise RuntimeError("'BOT_TOKEN' environment variable is not set")

    configure_logging(debug=args.debug, verbose=args.verbose)

    guild_config = GuildConfig.model_validate_json(args.config_file.read_text(encoding="UTF-8"))

    async def configure_guild(guild: discord.Guild) -> None:
        configurator = GuildConfigurator(guild)
        await configurator.apply_configuration(guild_config)

    bot = GuildConfigurationBot(args.guild_id, configure_guild)
    asyncio.run(run_bot(bot, bot_token))


if __name__ == "__main__":
    main()
