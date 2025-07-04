from pathlib import Path
import json

import yaml

from micromanager.models import System, Project, Service
from micromanager.config.errors import (
    ConfigFileDoesNotExistError,
    ComposeFileDoesNotExistError,
)


class Parser:
    """Parser for micromanager configuration file."""

    def __init__(self, paths: list[Path], json_parser=json, yaml_parser=yaml) -> None:
        self._paths = paths
        self._json = json_parser
        self._yaml = yaml_parser

    def parse(self) -> dict[str, System]:
        """Parse the configuration file into a dictionary."""
        for path in self._paths:
            if path.exists():
                return self._parse_config(path)

        raise ConfigFileDoesNotExistError(list(map(str, self._paths)))

    def _parse_config(self, path: Path) -> dict[str, System]:
        json_file = self._json.load(path)
        config = dict()

        for name, system in json_file["systems"].items():
            config[name] = self._build_system(name, system)

        return config

    def _build_system(self, name: str, attrs: dict) -> System:
        is_default = attrs.get("default", False)
        projects = [
            self._build_project(p_name, p) for p_name, p in attrs["projects"].items()
        ]

        system = System(name=name, is_default=is_default, projects=projects)
        return system

    def _build_project(self, name: str, attrs: dict) -> Project:
        compose_file_path = Path(attrs["compose_file_path"])
        if not compose_file_path.exists():
            raise ComposeFileDoesNotExistError(name, str(compose_file_path))

        services = self._build_services(compose_file_path)

        project = Project(
            name=name, compose_file_path=compose_file_path, services=services
        )
        return project

    def _build_services(self, compose_file_path: Path) -> list[Service]:
        compose_file = self._yaml.load(compose_file_path)

        services = [Service(name=s) for s in compose_file["services"]]
        return services
