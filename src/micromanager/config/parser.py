import os
from pathlib import Path
from typing import Optional, Protocol
from dataclasses import replace

import json
import yaml
from rlist import rlist

from micromanager.models import System, Project, Service
from micromanager.config.models import ConfiguredSystem
from micromanager.config.errors import (
    ConfigFileDoesNotExistError,
    ComposeFileDoesNotExistError,
    InvalidConfigFileError,
)


class FileParser(Protocol):
    """
    A parser used to parse json or yaml files.
    """

    def load(self, path: Path) -> dict: ...


class JsonParser:
    """
    Parser for json files.
    Used to parse the micromanager configuration.
    """

    def __init__(self) -> None:
        self._json = json

    def load(self, path: Path) -> dict:
        """
        Parse and load the file in the given path in a dictionary.
        """
        with open(os.path.expandvars(path), "r") as f:
            try:
                parsed = self._json.load(f)
            except json.decoder.JSONDecodeError as e:  # ty: ignore unresolved-attribute
                raise InvalidConfigFileError(str(path), str(e)) from None

        return parsed


class YamlParser:
    """
    Parser for yaml files.
    Used to parse docker compose configurations.
    """

    def __init__(self) -> None:
        self._yaml = yaml

    def load(self, path: Path) -> dict:
        """
        Parse and load the file in the given path in a dictionary.
        """
        with open(os.path.expandvars(path), "r") as f:
            parsed = self._yaml.load(f, yaml.Loader)

        return parsed


class Parser:
    """
    Parser for micromanager configuration file.
    Responsible for parsing the json config of micromanager and the
    yml docker compose configs.
    Also, validates for correct application logic configuration.
    """

    def __init__(
        self,
        path: Path,
        json_parser: Optional[FileParser] = None,
        yaml_parser: Optional[FileParser] = None,
    ) -> None:
        self._path = path
        self._effective_path: Optional[Path] = None
        self._json = JsonParser() if json_parser is None else json_parser
        self._yaml = YamlParser() if yaml_parser is None else yaml_parser

    def parse(self) -> dict[str, System]:
        """Parse the configuration file into a dictionary."""
        if self._path.exists(follow_symlinks=False):
            self._effective_path = self._path
            return self._parse_config()

        raise ConfigFileDoesNotExistError(str(self._path))

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

        projects = rlist()
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

        compose_file_path = Path(os.path.expandvars(attrs["compose_file_path"]))
        if not compose_file_path.exists():
            raise ComposeFileDoesNotExistError(name, str(compose_file_path))

        services = self._build_services(compose_file_path)

        project = Project(
            name=name, compose_file_path=compose_file_path, services=services
        )
        return project

    def _build_services(self, compose_file_path: Path) -> rlist[Service]:
        compose_file = self._yaml.load(compose_file_path)

        services = rlist([Service(name=s) for s in compose_file["services"]])
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
