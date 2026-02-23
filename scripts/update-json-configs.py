import importlib
import sys
from pathlib import Path

from discord_guild_configurator.models import GuildConfig

exit_code = 0

configs_dir = Path(__file__).parent.parent / "configs"
sys.path.append(str(configs_dir.absolute()))
for config_py_file in Path("configs").glob("*.py"):
    # load config from file
    config_module = importlib.import_module(config_py_file.stem)
    config = getattr(config_module, "CONFIG", None)

    if config is None:
        exit_code = 1
        print(f"{config_py_file.name}: No variable 'CONFIG' found")
        continue

    if not isinstance(config, GuildConfig):
        exit_code = 1
        print(f"{config_py_file.name}: Variable 'CONFIG' is not of type GuildConfig")
        continue

    new_config_str = config.model_dump_json(indent=2)
    if not new_config_str.endswith("\n"):
        new_config_str += "\n"

    config_json_file = config_py_file.with_suffix(".json")
    if config_json_file.exists() and config_json_file.read_text(encoding="UTF-8") == new_config_str:
        print(f"JSON config is up-to-date: {config_json_file.name}")
        continue

    exit_code = 1
    config_json_file.write_text(new_config_str, encoding="UTF-8")
    print(f"Updated JSON config: {config_json_file.name}")
