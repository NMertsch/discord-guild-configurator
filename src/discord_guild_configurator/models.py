from __future__ import annotations

import re
import textwrap
from typing import Annotated, Literal, Self

from pydantic import AfterValidator, BaseModel, Field, model_validator

MultilineString = Annotated[
    str,
    AfterValidator(lambda text: textwrap.dedent(text.strip("\r\n").rstrip())),
]

Permission = Literal[
    "add_reactions",
    "administrator",
    "attach_files",
    "ban_members",
    "change_nickname",
    "connect",
    "create_events",
    "create_expressions",
    "create_instant_invite",
    "create_polls",
    "create_private_threads",
    "create_public_threads",
    "deafen_members",
    "embed_links",
    "external_emojis",
    "external_stickers",
    "kick_members",
    "manage_channels",
    "manage_emojis",
    "manage_emojis_and_stickers",
    "manage_events",
    "manage_expressions",
    "manage_guild",
    "manage_messages",
    "manage_nicknames",
    "manage_permissions",
    "manage_roles",
    "manage_threads",
    "manage_webhooks",
    "mention_everyone",
    "moderate_members",
    "move_members",
    "mute_members",
    "priority_speaker",
    "read_message_history",
    "read_messages",
    "request_to_speak",
    "send_messages",
    "send_messages_in_threads",
    "send_polls",
    "send_tts_messages",
    "send_voice_messages",
    "speak",
    "stream",
    "use_application_commands",
    "use_embedded_activities",
    "use_external_apps",
    "use_external_emojis",
    "use_external_sounds",
    "use_external_stickers",
    "use_soundboard",
    "use_voice_activation",
    "view_audit_log",
    "view_channel",
    "view_creator_monetization_analytics",
    "view_guild_insights",
]


class PermissionOverwrite(BaseModel):
    roles: list[str]
    allow: list[Permission] = Field(default_factory=list)
    deny: list[Permission] = Field(default_factory=list)


class ForumChannel(BaseModel):
    type: Literal["forum"] = "forum"

    name: str
    topic: MultilineString
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)

    tags: list[str] = Field(default_factory=list)
    require_tag: bool = False


class TextChannel(BaseModel):
    type: Literal["text"] = "text"

    name: str
    topic: MultilineString
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)

    channel_messages: list[MultilineString] = Field(default_factory=list)


class VoiceChannel(BaseModel):
    type: Literal["voice"] = "voice"

    name: str
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)


class Category(BaseModel):
    name: str
    channels: list[
        Annotated[TextChannel | ForumChannel | VoiceChannel, Field(discriminator="type")]
    ]
    permission_overwrites: list[PermissionOverwrite] = Field(default_factory=list)


class Role(BaseModel):
    name: str
    color: str = Field(pattern=re.compile("^#[0-9A-F]{6}$"))
    hoist: bool = False
    mentionable: bool = False
    permissions: list[Permission] = Field(default_factory=list)


class GuildConfig(BaseModel):
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
