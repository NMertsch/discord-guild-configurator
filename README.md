# Configure a Discord guild

This program configures a Discord guild based on a given configuration.

See [ep2025_config.py](./src/discord_guild_configurator/configs/ep2025_config.py) for an example configuration.
It is the configuration of the EuroPython 2025 conference server.

## Features

Features:
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
    - Update the 'mandatory/optional' state of forum tags
    - Update category, text channel, and forum permission overwrites
- Update category and channel permission overwrites
- Update channel's default messages

Deliberate omissions:
- Delete roles
- Delete categories
- Delete channels
- Delete forum tags
- Delete human-authored messages

All operations are idempotent. Applying the same configuration twice will perform no changes.

## Planned features

- Guild configurator: Configure role order. Currently, this requires manual intervention.
- Guild configurator CLI: Read configuration from a file. Currently, the EP2025 configuration is hardcoded.
- New program: Export the configuration of an existing guild.

## Usage instructions

### Discord setup

Create a Discord bot with the privileges for receiving `GUILD_MEMBER` events on the target guild.

### Command-line usage

* Set the environment variable `BOT_TOKEN` to the bot's access token.
* Install this package, e.g., with `pip install .` or `uv sync`.
* CLI: Run `discord-guild-configurator --guild-id <GUILD_ID>`. You can use `--verbose` or `--debug` to see more output.

NOTE: This will apply the [EuroPython 2025 configuration](./src/discord_guild_configurator/configs/ep2025_config.py)
to the specified guild.
See below for instructions on how to configure the guild with your own configuration.

### Programmatic usage

```python
# Option 1: Create guild configuration programmatically
from discord_guild_configurator.models import GuildConfig

GUILD_CONFIG = GuildConfig(...)

# Option 2: Load guild configuration from a JSON file
import json
from pathlib import Path

from discord_guild_configurator.models import GuildConfig

config_file = Path("guild_config.json")
config_file_content = config_file.read_text(encoding="UTF-8")
GUILD_CONFIG = GuildConfig.model_validate_json(config_file_content)

# Apply the configuration
from discord_guild_configurator.bot import GuildConfigurationBot, run_bot

BOT_TOKEN = "..."
GUILD_ID = 123456789

configurator = GuildConfigurationBot(GUILD_ID, GUILD_CONFIG)
run_bot(configurator, BOT_TOKEN)
```

## Development

This project uses the following tools:

* [uv](https://docs.astral.sh/uv/) for Python project and dependency management
* [ruff](https://docs.astral.sh/ruff/) for Python code linting and formatting
* [ty](https://docs.astral.sh/ty/) for Python type checking
* [prek](https://prek.j178.dev/) for running code checks on each commit and in CI
* [GitHub Actions](https://docs.github.com/en/actions) for continuous integration
