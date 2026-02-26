from __future__ import annotations

import re
import textwrap
from typing import Annotated, Literal, Self

import discord
from pydantic import (
    AfterValidator,
    Field,
    model_validator,
)

from discord_guild_configurator._utils import StrictBaseModel
from discord_guild_configurator.generated_models import (
    ContentFilter,
    Locale,
    NotificationLevel,
    Permissions,
    VerificationLevel,
)

MultilineString = Annotated[
    str,
    AfterValidator(lambda text: textwrap.dedent(text.strip("\r\n").rstrip())),
]


class PermissionOverwrite(StrictBaseModel):
    roles: list[str]
    allow: list[Permissions] = Field(default_factory=list)
    deny: list[Permissions] = Field(default_factory=list)


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
    permissions: list[Permissions] = Field(default_factory=list)


class CommunityFeatures(StrictBaseModel):
    guild_description: str | None
    rules_channel: str
    public_updates_channel: str
    safety_alerts_channel: str


class SystemChannel(StrictBaseModel):
    name: str
    guild_reminder_notifications: bool
    join_notification_replies: bool
    join_notifications: bool
    premium_subscriptions: bool
    role_subscription_purchase_notification_replies: bool
    role_subscription_purchase_notifications: bool


class GuildConfig(StrictBaseModel):
    roles: list[Role]
    system_channel: SystemChannel
    categories: list[Category]
    community_features: CommunityFeatures | None
    verification_level: VerificationLevel
    default_notifications: NotificationLevel
    explicit_content_filter: ContentFilter
    preferred_locale: Locale

    @model_validator(mode="after")
    def verify_system_channel_names(self) -> Self:
        channel_names: list[str] = []
        for category in self.categories:
            channel_names.extend(channel.name for channel in category.channels)

        required_channels = [self.system_channel.name]
        if self.community_features:
            required_channels.extend(
                [
                    self.community_features.rules_channel,
                    self.community_features.public_updates_channel,
                    self.community_features.safety_alerts_channel,
                ]
            )
        missing_channels = [
            channel for channel in required_channels if channel not in channel_names
        ]

        if missing_channels:
            raise ValueError(f"Missing system channels: {missing_channels}")

        return self

    @model_validator(mode="after")
    def verify_verification_level(self) -> Self:
        if self.community_features and self.verification_level < discord.VerificationLevel.medium:  # type: ignore[unsupported-operator]
            raise ValueError(
                "The Community feature requires a verification level of at least medium"
            )
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
