from pathlib import Path
from typing import Optional

from micromanager.models import System
from micromanager.config.parser import Parser


class AppConfig:
    """ """

    _PATH: list[Path] = [
        Path("$HOME/.config/micromanager/config.json"),
        Path("/usr/local/etc/micromanager/config.json"),
    ]

    def __init__(self, parser=None) -> None:
        self._config: Optional[dict[str, System]] = None
        self._default_system: Optional[System] = None
        self._current_system: Optional[System] = None
        self._parser: Parser = Parser(self._PATH) if parser is None else parser

    def get_default_system(self) -> System:
        """ """
        if self._default_system is None:
            self._default_system = self._find_default_system()

        return self._default_system

    def get_current_system(self) -> System:
        """ """
        if self._current_system is None:
            self._current_system = self._find_current_system()

        return self._current_system

    def set_current_system(self, system: System) -> None:
        """ """
        self._current_system = system

    def _find_default_system(self) -> System:
        config = self._get_config()
        for system in config.systems:
            if system.default:
                return system

    def _find_current_system(self) -> System:
        if self._current_system is None:
            self._current_system = self.get_default_system()

        return self._current_system

    def _get_config(self) -> dict:
        if self._config is None:
            self._config = self._parser.parse()

        return self._config
