from pathlib import Path
from typing import Optional
import os

from platformdirs import user_config_dir

from micromanager.models import System
from micromanager.config.parser import Parser
from micromanager.config.errors import NoDefaultSystemError


class AppConfig:
    """
    Configuration object for the micromanager tool.
    Defines helper methods to interact with the configuration.
    """

    def __init__(self, parser=None) -> None:
        self._path = None
        self._config: Optional[dict[str, System]] = None
        self._default_system: Optional[System] = None
        self._current_system: Optional[System] = None
        self._parser: Parser = (
            Parser(self.config_file_path()) if parser is None else parser
        )

    @property
    def systems(self) -> dict[str, System]:
        """
        Returns all configured systems as a dictionary with system name as key
        and system as value.
        """
        return self._get_config()

    def get_default_system(self) -> System:
        """
        Get the default micromanager system.
        If only one system is configured, that is the default one.
        """
        if self._default_system is None:
            self._default_system = self._get_default_system()

        return self._default_system

    def get_current_system(self) -> System:
        """
        Get the current system, i.e. the system that is currently selected.
        If a specific system is not selected, then the default system is set as the current system.
        All commands of the micromanager CLI are directed to the current system.
        """
        if self._current_system is None:
            self._current_system = self._get_current_system()

        return self._current_system

    def set_current_system(self, system: System) -> None:
        """
        Set the current system, i.e. the system that is currently selected.
        All commands of the micromanager CLI are directed to the current system.
        """
        self._current_system = system

    def config_file_path(self) -> Path:
        """
        Return the path of the micromanager configuration file.

        The path can be set from the enviroment variable MICROMANAGER_CONFIG_PATH.
        If not set it defaults to a sensible value according to the operating system.
        """
        if self._path is None:
            self._path = self._get_config_file_path()

        return self._path

    def _get_default_system(self) -> System:
        config = self._get_config()
        for system in config.values():
            if system.is_default:
                return system

        raise NoDefaultSystemError()

    def _get_current_system(self) -> System:
        if self._current_system is None:
            self._current_system = self.get_default_system()

        return self._current_system

    def _get_config(self) -> dict:
        if self._config is None:
            self._config = self._parser.parse()

        return self._config

    def _get_config_file_path(self) -> Path:
        env_var = os.getenv("MICROMANAGER_CONFIG_PATH", None)

        if env_var is not None:
            return Path(os.path.expandvars(env_var))

        return Path(user_config_dir("micromanager"), "config.json")
