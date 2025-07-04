from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class Service:
    name: str


@dataclass(frozen=True, kw_only=True)
class Project:
    name: str
    compose_file_path: Path
    services: list[Service]


@dataclass(frozen=True, kw_only=True)
class System:
    name: str
    is_default: bool
    projects: list[Project]
