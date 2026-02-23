"""Update exported JSON schema if necessary."""

import json
import sys
from pathlib import Path

from discord_guild_configurator.models import GuildConfig

schema_file = Path(__file__).parent.parent / "discord_guild_config.schema.json"

new_schema = GuildConfig.model_json_schema(mode="validation")
new_schema_str = json.dumps(new_schema, indent=2)

# ensure trailing newline
if new_schema_str.endswith("}"):
    new_schema_str += "\n"

if schema_file.exists() and schema_file.read_text(encoding="UTF-8") == new_schema_str:
    print(f"JSON schema is up-to-date: {schema_file.name}")
    sys.exit(0)

schema_file.write_text(new_schema_str, encoding="UTF-8", newline="\n")
print(f"Updated JSON schema: {schema_file.name}")
sys.exit(1)
