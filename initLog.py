import os
import json
import logging
from typing import Any, Dict


def init_log() -> None:
    """
    Initializes the logging configuration based on the config.json file.

    This function reads the logging file path from the configuration file
    and sets up the logging system accordingly. If the log file already exists,
    it will be deleted before initializing.

    Raises:
        FileNotFoundError: If the config.json file does not exist.
        KeyError: If 'logging_output_file' key is missing in the config.
        json.JSONDecodeError: If config.json is not a valid JSON.
    """
    try:
        with open("config.json", "r", encoding="utf-8") as config_file:
            config: Dict[str, Any] = json.load(config_file)
            log_file: str = config['logging_output_file']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to initialize logger: {e}")

    if os.path.exists(log_file):
        os.remove(log_file)

    logging.basicConfig(
        filename=log_file,
        encoding="utf-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )

