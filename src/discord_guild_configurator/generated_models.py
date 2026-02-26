from typing import Annotated, Literal

import discord
import pydantic

Permissions = Literal[
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
VerificationLevel = Annotated[
    discord.VerificationLevel,
    pydantic.PlainValidator(
        lambda value: discord.VerificationLevel[value] if isinstance(value, str) else value
    ),
    pydantic.PlainSerializer(lambda value: value.name),
    pydantic.Field(
        json_schema_extra={
            "enum": [option.name for option in discord.VerificationLevel],
            "type": "string",
        },
    ),
]
NotificationLevel = Annotated[
    discord.NotificationLevel,
    pydantic.PlainValidator(
        lambda value: discord.NotificationLevel[value] if isinstance(value, str) else value
    ),
    pydantic.PlainSerializer(lambda value: value.name),
    pydantic.Field(
        json_schema_extra={
            "enum": [option.name for option in discord.NotificationLevel],
            "type": "string",
        },
    ),
]
Locale = Annotated[
    discord.Locale,
    pydantic.PlainValidator(
        lambda value: discord.Locale[value] if isinstance(value, str) else value
    ),
    pydantic.PlainSerializer(lambda value: value.name),
    pydantic.Field(
        json_schema_extra={
            "enum": [option.name for option in discord.Locale],
            "type": "string",
        },
    ),
]
ContentFilter = Annotated[
    discord.ContentFilter,
    pydantic.PlainValidator(
        lambda value: discord.ContentFilter[value] if isinstance(value, str) else value
    ),
    pydantic.PlainSerializer(lambda value: value.name),
    pydantic.Field(
        json_schema_extra={
            "enum": [option.name for option in discord.ContentFilter],
            "type": "string",
        },
    ),
]
