import json
import pathlib
from warnings import warn
from pathlib import Path
import os

from structs.global_vars import GlobalVariables


def get_config_file(config_path_string: str, config_file_name = "config.json"):
    config_location = Path(config_path_string).expanduser().resolve()

    try:
        # If the config location passed is the name of the config file in the current working directory
        # Or the full path, this will open it either way
        with open(config_location, mode="r") as config_file:
            config = json.loads(config_file.read())
        # If it's a directory we'll try to load config_location/config_file_name as the config file
    except IsADirectoryError:
        with open(os.path.join(config_location, config_file_name), mode="r") as config_file:
            config = json.loads(config_file.read())
    except Exception as e:
        warn("Error finding and loading config file, using default config")
        return GlobalVariables().config
    return config


class Config:

    def __find_config_folder__(self):
        if self.__config_location__ is not None:
            # Deal with argparse passing strings in as lists with 1 entry
            if isinstance(self.__config_location__, list):
                self.__config_location__ = self.__config_location__[0]
        else:
            self.__config_location__ = self.__default_config_name__

        path = Path(self.__config_location__).expanduser().absolute()
        if not path.exists():
            raise FileNotFoundError("Could not find a file or folder at " + self.__config_location__)
        if path.is_dir():
            path = pathlib.Path.joinpath(path, self.__default_config_name__)
            if path.is_file():
                self.__load_config__(path)
            else:
                raise FileNotFoundError(
                    "Could not find config file named " + self.__default_config_name__ + " in folder " +
                    self.__config_location__)
        elif path.is_file():
            self.__load_config__(path)

    def __load_config__(self, path):
        with path.open(mode="r") as file:
            self.config = json.loads(file.read())

    def __init__(self, config_location, default_config_name="config.json"):
        # Argparse currently passes in arguments of certain types wrapped in a list when it shouldn't
        # This is workaround for that issue

        # If config_location is a folder, this option specifies what file to look for in the folder as the config

        if self.__config_location__ is not None:
            # Deal with argparse passing strings in as lists with 1 entry
            if isinstance(self.__config_location__, list):
                self.__config_location__ = self.__config_location__[0]
        else:
            self.__config_location__ = self.__default_config_name__

        self.config = get_config_file(config_location, default_config_name)
