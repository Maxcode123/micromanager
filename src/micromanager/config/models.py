from dataclasses import dataclass
from typing import Optional

from rlist import rlist

from micromanager.models import System, Project


@dataclass
class ConfiguredSystem:
    """
    A system as defined in the configuration file with its primitive values,
    before it is casted into a domain model.
    """

    name: str
    is_default: Optional[bool]
    projects: rlist[Project]

    def to_system(self) -> System:
        """
        Convert the configuration model into a domain model with the provided
        values.
        """
        is_default = False if self.is_default is None else self.is_default
        return System(name=self.name, is_default=is_default, projects=self.projects)
