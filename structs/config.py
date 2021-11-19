import json
from warnings import warn
from pathlib import Path
import os

from structs.global_vars import GlobalVariables


def open_config(config_location):
    with config_location.open(mode="r") as config_file:
        return json.loads(config_file.read())


def get_config_file(config_path_string, default_config_name):
    # Argparse currently passes in arguments of certain types wrapped in a list when it shouldn't
    # This is workaround for that issue
    if config_path_string is not None:
        # Deal with argparse passing strings in as lists with 1 entry
        if isinstance(config_path_string, list):
            config_path_string = config_path_string[0]
    else:
        config_path_string = default_config_name

    config_location = Path(config_path_string).expanduser().resolve()

    try:
        # If it's a directory we'll try to load config_location/config_file_name as the config file
        warning_message = "Error finding and loading config file at \"" + config_location.__str__() + "\", using default config"
        if config_location.is_dir():
            warning_message = "Error finding and loading config file named \"" + default_config_name + "\" located in \"" + config_location.__str__() + "\", using default config"
            config_location = Path.joinpath(config_location, default_config_name)
        config = open_config(config_location)
    except FileNotFoundError:
        warn(warning_message)
        return GlobalVariables().config
    return config


class Config:
    def __init__(self, config_location, default_config_name="config.json"):
        # If config_location is a folder, this option specifies what file to look for in the folder as the config

        self.config = get_config_file(config_location, default_config_name=default_config_name)
