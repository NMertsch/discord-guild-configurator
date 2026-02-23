from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, Any, Final

import discord
from discord import Guild
from discord.ext.commands import Bot

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


logger = logging.getLogger(__name__)


class GuildConfigurationBot(Bot):
    def __init__(self, guild_id: int, action: Callable[[Guild], Awaitable[None]]) -> None:
        """Discord bot which exports all guild members to .csv files and then stops itself."""
        intents = discord.Intents.all()
        intents.presences = False
        super().__init__(intents=intents, command_prefix="$")

        self.guild_id: Final[int] = guild_id
        self.action: Final[Callable[[Guild], Awaitable[None]]] = action

    async def on_ready(self) -> None:
        """Event handler for successful connection."""
        guild = self.get_guild(self.guild_id)
        if guild is None:
            raise RuntimeError(f"Could not find guild with ID {self.guild_id}")
        await self.action(guild)

        await self.close()

    async def on_error(self, event: str, /, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401 (Any)
        """Event handler for uncaught exceptions."""
        exc_type, exc_value, _exc_traceback = sys.exc_info()
        if exc_type is None:
            logger.error(f"Unknown error during {event}(*{args}, **{kwargs})")
        else:
            logger.error(f"{exc_type.__name__} {exc_value}")

        # let discord.py log the exception
        await super().on_error(event, *args, **kwargs)

        await self.close()


async def run_bot(bot: Bot, token: str) -> None:
    """Run a Discord bot."""
    async with bot as _bot:
        try:
            await _bot.login(token)
            await _bot.connect()
        except discord.LoginFailure:
            logger.exception("Invalid Discord bot token")
        except discord.PrivilegedIntentsRequired:
            logger.exception(
                "Insufficient privileges! "
                "Make sure the bot is allowed to receive 'GUILD_MEMBERS' events, "
                "and that its role is directly below the 'Admin' role."
            )
