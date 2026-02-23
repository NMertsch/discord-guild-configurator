from __future__ import annotations

import re
import textwrap
from typing import Annotated, Literal, Self

from pydantic import AfterValidator, Field, model_validator

from discord_guild_configurator._utils import StrictBaseModel
from discord_guild_configurator.generated_models import Permission

MultilineString = Annotated[
    str,
    AfterValidator(lambda text: textwrap.dedent(text.strip("\r\n").rstrip())),
]


class PermissionOverwrite(StrictBaseModel):
    roles: list[str]
    allow: list[Permission] = Field(default_factory=list)
    deny: list[Permission] = Field(default_factory=list)


class ForumChannel(StrictBaseModel):
    type: Literal["forum"] = "forum"

    name: str
    topic: MultilineString
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)

    tags: list[str] = Field(default_factory=list)
    require_tag: bool = False


class TextChannel(StrictBaseModel):
    type: Literal["text"] = "text"

    name: str
    topic: MultilineString
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)

    channel_messages: list[MultilineString] = Field(default_factory=list)


class VoiceChannel(StrictBaseModel):
    type: Literal["voice"] = "voice"

    name: str
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)


class Category(StrictBaseModel):
    name: str
    channels: list[
        Annotated[TextChannel | ForumChannel | VoiceChannel, Field(discriminator="type")]
    ]
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)


class Role(StrictBaseModel):
    name: str
    color: str = Field(pattern=re.compile("^#[0-9A-F]{6}$"))
    hoist: bool = False
    mentionable: bool = False
    permissions: list[Permission] = Field(default_factory=list)


class GuildConfig(StrictBaseModel):
    roles: list[Role]
    rules_channel_name: str
    system_channel_name: str
    updates_channel_name: str
    categories: list[Category]

    @model_validator(mode="after")
    def verify_system_channel_names(self) -> Self:
        channel_names: list[str] = []
        for category in self.categories:
            channel_names.extend(channel.name for channel in category.channels)

        required_channels = [
            self.rules_channel_name,
            self.system_channel_name,
            self.updates_channel_name,
        ]
        missing_channels = [
            channel for channel in required_channels if channel not in channel_names
        ]

        if missing_channels:
            raise ValueError(f"Missing system channels: {missing_channels}")

        return self

    @model_validator(mode="after")
    def verify_permission_roles(self) -> Self:
        roles = [role.name for role in self.roles]

        missing_roles = set()
        for category in self.categories:
            for overwrite in category.permission_overwrites:
                for role in overwrite.roles:
                    if role not in roles:
                        missing_roles.add(role)
            for channel in category.channels:
                for overwrite in channel.permission_overwrites:
                    for role in overwrite.roles:
                        if role not in roles:
                            missing_roles.add(role)

        if missing_roles:
            raise ValueError(f"Missing roles: {missing_roles}")

        return self
