from pathlib import Path
from typing import Optional
from dataclasses import replace

import json
import yaml

from micromanager.models import System, Project, Service
from micromanager.config.models import ConfiguredSystem
from micromanager.config.errors import (
    ConfigFileDoesNotExistError,
    ComposeFileDoesNotExistError,
    InvalidConfigFileError,
)


class Parser:
    """
    Parser for micromanager configuration file.
    Responsible for parsing the json config of micromanager and the
    yml docker compose configs.
    Also, validates for correct application logic configuration.
    """

    def __init__(self, paths: list[Path], json_parser=json, yaml_parser=yaml) -> None:
        self._paths = paths
        self._effective_path: Optional[Path] = None
        self._json = json_parser
        self._yaml = yaml_parser

    def parse(self) -> dict[str, System]:
        """Parse the configuration file into a dictionary."""
        for path in self._paths:
            if path.exists():
                self._effective_path = path
                return self._parse_config()

        raise ConfigFileDoesNotExistError(list(map(str, self._paths)))

    def _parse_config(self) -> dict[str, System]:
        json_file = self._json.load(self._effective_path)
        config = dict()

        if "systems" not in json_file.keys():
            raise InvalidConfigFileError(
                self._effective_path, "'systems' field does not exist in config.json"
            )

        systems = json_file["systems"]

        if not isinstance(systems, dict):
            raise InvalidConfigFileError(
                self._effective_path,
                "The value of the systems field is not a valid object",
            )

        for name, system in json_file["systems"].items():
            if not isinstance(system, dict):
                raise InvalidConfigFileError(
                    self._effective_path, f"The system '{name}' is not a valid object"
                )
            config[name] = self._build_system(name, system)

        self._validate_config(config)
        config = {name: sys.to_system() for name, sys in config.items()}

        if len(config) == 1:
            config[name] = replace(config[name], is_default=True)

        return config

    def _build_system(self, name: str, attrs: dict) -> ConfiguredSystem:
        is_default = attrs.get("default", None)

        if "projects" not in attrs:
            raise InvalidConfigFileError(
                self._effective_path,
                f"'projects' field does not exist in the '{name}' system",
            )

        projects = []
        for project_name, project_attrs in attrs["projects"].items():
            if not isinstance(project_attrs, dict):
                raise InvalidConfigFileError(
                    self._effective_path,
                    f"The project '{project_name}' of system '{name}' is not a valid object",
                )
            projects.append(self._build_project(project_name, project_attrs))

        system = ConfiguredSystem(name=name, is_default=is_default, projects=projects)
        return system

    def _build_project(self, name: str, attrs: dict) -> Project:
        if "compose_file_path" not in attrs:
            raise InvalidConfigFileError(
                self._effective_path,
                f"Project '{name}' does not contain a 'compose_file_path' field",
            )

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

    def _validate_config(self, config: dict[str, System]) -> None:
        defaults = {sys_name for sys_name, sys in config.items() if sys.is_default}
        if len(defaults) > 1:
            raise InvalidConfigFileError(
                self._effective_path,
                f"More than one default systems configured ({defaults}); only one system can be the default",
            )

        if len(config) > 1 and len(defaults) == 0:
            raise InvalidConfigFileError(
                self._effective_path,
                'One system must be the default; set "default"="true"',
            )

        if len(config) == 1 and list(config.values())[0].is_default is False:
            sys_name = list(config.keys())[0]
            raise InvalidConfigFileError(
                self._effective_path,
                f'\'{sys_name}\' must be the default system since it is the only one. set "default"="true"',
            )
