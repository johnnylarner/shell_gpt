from typing import Dict
from pathlib import Path
from dotenv import dotenv_values


DEFAULT_CACHE_AND_API_CONFIG = {
    "MAX_CHAT_MESSAGES": 50,
    "MAX_CACHE_LENGTH": 200,
    "API_KEY": "",
    "API_ENDPOINT": "https://api.openai.com/v1/chat/completions",
}


def get_legacy_api_key_if_exists(api_key_path: Path) -> str:
    if api_key_path.exists():
        return api_key_path.read_text().strip()
    return ""


def make_config_string_from_user_input_or_defaults(legacy_api_key: str) -> str:
    """Returns a string containing user or default config
    data for ChatGPT caching and API settings.
    """

    DEFAULT_CACHE_AND_API_CONFIG["API_KEY"] = legacy_api_key
    config_string = ""
    for setting in DEFAULT_CACHE_AND_API_CONFIG:
        default_value = DEFAULT_CACHE_AND_API_CONFIG[setting]
        user_value = input(f"Please enter a value for {setting} [{default_value}]: ")
        value = user_value if user_value else default_value
        config_string += f"{setting}={value}\n"

    return config_string


def write_config_string_to_path(config_string: str, config_path: Path) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(config_string)


def initialize_cache_and_api_config(config_path: Path, api_key_path: Path) -> None:
    legacy_api_key = get_legacy_api_key_if_exists(api_key_path)
    config_string = make_config_string_from_user_input_or_defaults(
        legacy_api_key=legacy_api_key
    )
    write_config_string_to_path(config_string, config_path)


def get_cache_and_api_config(config_path: Path, api_key_path: Path) -> Dict[str, str]:
    if not config_path.exists():
        initialize_cache_and_api_config(config_path, api_key_path)

    cache_and_api_config = dotenv_values(str(config_path))
    return cache_and_api_config
