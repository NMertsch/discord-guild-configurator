from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import Final, assert_never

import discord
from discord import VerificationLevel
from discord.utils import get as discord_get

from discord_guild_configurator.models import (
    Category,
    CommunityFeatures,
    ForumChannel,
    GuildConfig,
    PermissionOverwrite,
    Role,
    SystemChannel,
    TextChannel,
    VoiceChannel,
)

logger = logging.getLogger(__name__)


class GuildConfigurator:
    def __init__(self, guild: discord.Guild) -> None:
        self.guild: Final[discord.Guild] = guild

    async def apply_configuration(self, template: GuildConfig) -> None:
        self._check_config_compatibility(template)

        logger.info("Configuring roles")
        for role_template in template.roles:
            await self.ensure_role(role_template)

        logger.info("Configuring system channel")
        await self.ensure_system_channel(template.system_channel)

        if template.community_features:
            logger.info("Configuring 'COMMUNITY' features")
            await self.ensure_community_feature(template.community_features)

        logger.info("Configuring categories and channels")
        await self.ensure_categories_and_channels(template.categories)

        logger.info("Configuring permissions")
        await self.ensure_category_and_channel_permissions(template.categories)

        logger.info("Configure channel topics")
        await self.ensure_channel_topics(template.categories)

        logger.info("Configure channel default messages")
        await self.ensure_default_messages(template.categories)

    def _check_config_compatibility(self, template: GuildConfig) -> None:
        if (
            "COMMUNITY" in self.guild.features
            and template.verification_level < discord.VerificationLevel.medium  # type: ignore[unsupported-operator]
        ):
            raise ValueError(
                "The Community feature requires a verification level of at least medium"
            )

    def get_text_channel(self, name: str) -> discord.TextChannel:
        channel = discord_get(self.guild.text_channels, name=name)
        if channel is None:
            raise RuntimeError(f"Could not find text channel with name '{name}'")
        return channel

    def get_forum(self, name: str) -> discord.ForumChannel:
        channel = discord_get(self.guild.forums, name=name)
        if channel is None:
            raise RuntimeError(f"Could not find forum with name '{name}'")
        return channel

    def get_channel(
        self, name: str
    ) -> discord.TextChannel | discord.ForumChannel | discord.VoiceChannel:
        channel = discord_get(self.guild.channels, name=name)
        if channel is None or not isinstance(
            channel, (discord.TextChannel, discord.ForumChannel, discord.VoiceChannel)
        ):
            raise RuntimeError(f"Could not find text, forum, or voice channel with name '{name}'")
        return channel

    def get_role(self, name: str) -> discord.Role:
        role = discord_get(self.guild.roles, name=name)
        if role is None:
            raise RuntimeError(f"Could not find role with name '{name}'")
        return role

    def get_category(self, name: str) -> discord.CategoryChannel:
        category = discord_get(self.guild.categories, name=name)
        if category is None:
            raise RuntimeError(f"Could not find category with name '{name}'")
        return category

    async def ensure_channel_permissions(
        self,
        channel: discord.TextChannel | discord.ForumChannel | discord.VoiceChannel,
        permission_overwrite_templates: list[PermissionOverwrite],
    ) -> None:
        logger.info("Ensure permissions for channel %s", channel.name)

        logger.debug("Accumulating expected permission overwrites")
        expected_overwrites_by_role: dict[str, dict[str, bool]] = defaultdict(dict)
        for overwrite_template in permission_overwrite_templates:
            for role_name in overwrite_template.roles:
                for permission in overwrite_template.allow:
                    expected_overwrites_by_role[role_name][permission] = True
                for permission in overwrite_template.deny:
                    expected_overwrites_by_role[role_name][permission] = False

        logger.debug("Determine if update is required")
        # Enabling some settings for some roles sometimes enables it also for @everyone.
        # Workaround: If any update is required, do a full update
        update_required = False
        updates_by_role: dict[discord.Role, discord.PermissionOverwrite] = {}
        for role_name, expected_overwrites in expected_overwrites_by_role.items():
            role = self.get_role(role_name)
            current_permissions = channel.permissions_for(role)
            for permission, expected in expected_overwrites.items():
                current_value = getattr(current_permissions, permission)
                if current_value != expected:
                    update_required = True
            updates_by_role[role] = discord.PermissionOverwrite(**expected_overwrites)

        if update_required:
            logger.debug("Update permissions")
            await channel.edit(overwrites=updates_by_role)

    async def ensure_category_and_channel_permissions(
        self, category_templates: list[Category]
    ) -> None:
        for category_template in category_templates:
            for channel_template in category_template.channels:
                channel = self.get_channel(channel_template.name)
                await self.ensure_channel_permissions(
                    channel,
                    category_template.permission_overwrites
                    + channel_template.permission_overwrites,
                )

    async def ensure_categories_and_channels(self, category_templates: list[Category]) -> None:
        # channel positions are global, not per-category
        channel_position = 0
        for category_position, category_template in enumerate(category_templates):
            await self.ensure_category(name=category_template.name, position=category_position)

            category = self.get_category(category_template.name)
            for channel_template in category_template.channels:
                if isinstance(channel_template, TextChannel):
                    await self.ensure_text_channel(
                        channel_template.name, category=category, position=channel_position
                    )
                elif isinstance(channel_template, VoiceChannel):
                    await self.ensure_voice_channel(
                        channel_template.name, category=category, position=channel_position
                    )
                elif isinstance(channel_template, ForumChannel):
                    await self.ensure_forum_channel(
                        channel_template.name,
                        category=category,
                        position=channel_position,
                        expected_tags=channel_template.tags,
                        require_tag=channel_template.require_tag,
                    )
                else:
                    # hint for the type checker: report error if there can be more channel types
                    assert_never(channel_template)

                channel_position += 1

    async def ensure_category(self, *, name: str, position: int) -> None:
        logger.info("Ensure category %s at position %d", name, position)
        category = discord_get(self.guild.categories, name=name)
        if category is None:
            logger.debug("Create category")
            await self.guild.create_category(name, position=position)
        else:
            logger.debug("Found category")
            if category.position != position:
                logger.debug("Update position")
                await category.edit(position=position)

    async def ensure_text_channel(
        self, name: str, *, category: discord.CategoryChannel | None, position: int
    ) -> None:
        logger.info("Ensure text channel %s at position %d", name, position)
        channel = discord_get(self.guild.text_channels, name=name)
        if channel is None:
            logger.debug("Create text channel %s", name)
            await self.guild.create_text_channel(name=name, category=category, position=position)
        else:
            logger.debug("Found text channel")
            if channel.category != category:
                logger.debug("Update category")
                await channel.edit(category=category)
            if channel.position != position:
                logger.debug("Update position")
                await channel.edit(position=position)

    async def ensure_voice_channel(
        self, name: str, *, category: discord.CategoryChannel | None, position: int
    ) -> None:
        logger.info("Ensure voice channel %s at position %d", name, position)
        channel = discord_get(self.guild.voice_channels, name=name)
        if channel is None:
            logger.debug("Create voice channel %s", name)
            await self.guild.create_voice_channel(name=name, category=category, position=position)
        else:
            logger.debug("Found voice channel")
            if channel.category != category:
                logger.debug("Update category")
                await channel.edit(category=category)
            if channel.position != position:
                logger.debug("Update position")
                await channel.edit(position=position)

    async def ensure_forum_channel(
        self,
        name: str,
        *,
        category: discord.CategoryChannel,
        position: int,
        expected_tags: list[str],
        require_tag: bool,
    ) -> None:
        logger.info("Configure forum channel %s at position %d", name, position)
        channel = discord_get(self.guild.forums, name=name)
        if channel is None:
            logger.debug("Create forum channel %s", name)
            channel = await self.guild.create_forum(name, category=category, position=position)
        else:
            logger.debug("Found forum channel")
            if channel.category is None or channel.category != category:
                logger.debug("Update category")
                await channel.edit(category=category)
            if channel.position != position:
                logger.debug("Update position")
                await channel.edit(position=position)

        await self.ensure_tags(channel, expected_tags, require_tag=require_tag)

    @staticmethod
    async def ensure_tags(
        channel: discord.ForumChannel, expected_tags: list[str], *, require_tag: bool
    ) -> None:
        logger.info("Ensure tags %s for channel %s", expected_tags, channel.name)
        existing_tags = {tag.name: tag for tag in channel.available_tags}
        tags_to_create = set(expected_tags) - set(existing_tags)

        if tags_to_create:
            for tag_name in tags_to_create:
                logger.debug("Create tag %s", tag_name)
                existing_tags[tag_name] = await channel.create_tag(name=tag_name)

            logger.debug("Update available tags for channel %s", channel.name)
            await channel.edit(available_tags=(list(existing_tags.values())))

        if require_tag and not channel.flags.require_tag:
            logger.debug("Update 'require_tag' flag")
            await channel.edit(require_tag=require_tag)

    async def ensure_role(self, template: Role) -> None:
        logger.info("Ensure role %s", template.name)
        permissions = discord.Permissions(
            **dict.fromkeys(template.permissions, True),
        )
        expected_color = discord.Color.from_str(template.color)

        role = discord_get(self.guild.roles, name=template.name)
        if role is None:
            logger.debug("Create role %s", template.name)
            await self.guild.create_role(
                name=template.name,
                colour=expected_color,
                hoist=template.hoist,
                mentionable=template.mentionable,
                permissions=permissions,
            )
        else:
            logger.debug("Found role")
            if role.name != "@everyone" and role.colour != expected_color:
                logger.debug("Update color")
                await role.edit(colour=expected_color)
            if role.hoist != template.hoist:
                logger.debug("Update hoist")
                await role.edit(hoist=template.hoist)
            if role.mentionable != template.mentionable:
                logger.debug("Update mentionable")
                await role.edit(mentionable=template.mentionable)
            if role.permissions != permissions:
                logger.debug("Update permissions")
                await role.edit(permissions=permissions)

    async def ensure_default_messages(self, categories: list[Category]) -> None:
        logger.info("Ensure default expected_messages")
        for category_template in categories:
            for channel_template in category_template.channels:
                if not isinstance(channel_template, TextChannel):
                    continue
                channel = self.get_text_channel(channel_template.name)
                expected_messages = await self.insert_mentions_into_messages(
                    channel_template.channel_messages
                )
                if expected_messages:
                    await self.ensure_channel_messages(channel, expected_messages)

    async def insert_mentions_into_messages(self, messages: list[str]) -> list[str]:
        logger.info("Insert mentions in messages")
        fixed_messages = []
        for message in messages:
            fixed_message = message
            for match in re.finditer("<<#([a-zA-Z0-9 _-]+)>>", message):
                channel = self.get_channel(match.group(1))
                logger.debug("Found mentioned channel %s", channel.name)
                fixed_message = fixed_message.replace(match.group(0), channel.mention)

            for match in re.finditer("<<@&([a-zA-Z0-9 _-]+)>>", message):
                role = self.get_role(match.group(1))
                logger.debug("Found mentioned role %s", role.name)
                fixed_message = fixed_message.replace(match.group(0), role.mention)

            fixed_messages.append(fixed_message)

        return fixed_messages

    @staticmethod
    async def ensure_channel_messages(channel: discord.TextChannel, messages: list[str]) -> None:
        logger.info("Ensure channel messages for channel %s", channel.name)
        existing_messages = []
        async for server_message in channel.history(limit=None, oldest_first=True):
            if not server_message.author.bot:
                logger.warning("Channel has messages from non-bot users, skipping message creation")
                return
            existing_messages.append(server_message)

        if [msg.content for msg in existing_messages] == messages:
            logger.debug("No update required")
            return

        for server_message in existing_messages:
            logger.debug("Deleting existing message")
            await server_message.delete()
        for new_message in messages:
            logger.debug("Send new message")
            await channel.send(content=new_message, suppress_embeds=True)

    async def ensure_channel_topics(self, category_templates: list[Category]) -> None:
        logger.info("Ensure channel topics")
        for category_template in category_templates:
            for channel_template in category_template.channels:
                if isinstance(channel_template, VoiceChannel):
                    continue  # voice channels have no topic
                channel = self.get_channel(channel_template.name)
                if isinstance(channel, discord.VoiceChannel):
                    continue  # voice channels have no topic
                expected_topic = channel_template.topic
                if channel.topic != expected_topic:
                    logger.debug("Update topic of channel %s", channel_template.name)
                    await channel.edit(topic=expected_topic)

    async def ensure_system_channel(self, system_channel: SystemChannel) -> None:
        logger.info("Ensure system channel configuration")
        current_system_channel = self.guild.system_channel
        if current_system_channel is None or current_system_channel.name != system_channel.name:
            logger.debug("Update system channel")
            new_system_channel = self.get_text_channel(system_channel.name)
            await self.guild.edit(system_channel=new_system_channel)

        target_flags = discord.SystemChannelFlags(
            join_notifications=system_channel.join_notifications,
            join_notification_replies=system_channel.join_notification_replies,
            guild_reminder_notifications=system_channel.guild_reminder_notifications,
            premium_subscriptions=system_channel.premium_subscriptions,
            role_subscription_purchase_notifications=system_channel.role_subscription_purchase_notifications,
            role_subscription_purchase_notification_replies=system_channel.role_subscription_purchase_notification_replies,
        )
        if self.guild.system_channel_flags != target_flags:
            logger.debug("Update system channel flags")
            await self.guild.edit(system_channel_flags=target_flags)

    async def ensure_community_feature(self, community_features: CommunityFeatures) -> None:
        logger.info("Ensure 'COMMUNITY' feature configuration")

        logger.debug("Ensure rules and public updates channels")
        if self.guild.verification_level < VerificationLevel.medium:  # type: ignore[unsupported-operator]
            logger.debug("Raise verification level at medium")
            await self.guild.edit(verification_level=discord.VerificationLevel.medium)

        if self.guild.default_notifications != discord.NotificationLevel.only_mentions:
            await self.guild.edit(default_notifications=discord.NotificationLevel.only_mentions)

        if "COMMUNITY" not in self.guild.features:
            logger.debug("Enable guild 'COMMUNITY' feature")
            await self.guild.edit(
                community=True,
                public_updates_channel=self.get_text_channel(
                    community_features.public_updates_channel
                ),
                rules_channel=self.get_text_channel(community_features.rules_channel),
                safety_alerts_channel=self.get_text_channel(
                    community_features.safety_alerts_channel
                ),
                description=community_features.guild_description,
                explicit_content_filter=discord.ContentFilter.all_members,
            )
