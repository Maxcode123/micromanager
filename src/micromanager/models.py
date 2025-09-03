from dataclasses import dataclass
from pathlib import Path

from rlist import rlist


@dataclass(frozen=True, kw_only=True)
class Service:
    name: str


@dataclass(frozen=True, kw_only=True)
class Project:
    name: str
    compose_file_path: Path
    services: rlist[Service]


@dataclass(frozen=True, kw_only=True)
class System:
    name: str
    is_default: bool
    projects: rlist[Project]
