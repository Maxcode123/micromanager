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

    def pretty_str(self) -> str:
        """
        Return a pretty-formatted string representation of a Project.
        """
        s = f"""name: {self.name}
                compose_file_path: {self.compose_file_path}
                services:"""
        s += "\n"
        for service in self.services:
            s += "\t\t\t" + service.name + "\n"

        return s


@dataclass(frozen=True, kw_only=True)
class System:
    name: str
    is_default: bool
    projects: list[Project]

    def pretty_str(self) -> str:
        """
        Return a pretty-formatted string representation of a System.
        """
        s = f"""name: {self.name}
        is_default: {self.is_default}
        projects:"""
        s += "\n"
        for project in self.projects:
            s += "\t\t" + project.pretty_str()

        return s
