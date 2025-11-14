from enum import Enum
from dataclasses import dataclass
from typing import TypeAlias

from python_on_whales import DockerClient, Container as _Container
from python_on_whales.exceptions import DockerException
from rlist import rlist

from micromanager.models import Project
from micromanager.compose.errors import DockerComposePsError


class Status(Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    RESTARTING = "RESTARTING"
    EXITED = "EXITED"
    PAUSED = "PAUSED"
    DEAD = "DEAD"


@dataclass
class Container:
    name: str
    status: Status


@dataclass
class DockerComposeProjectStatus:
    project_name: str
    containers: rlist[Container]


DockerComposePsResponse: TypeAlias = rlist[DockerComposeProjectStatus]


class DockerComposePs:
    """The docker compose ps command interface"""

    FLAGS = {
        "all": True,
    }

    @classmethod
    def call(cls, projects: rlist[Project]) -> DockerComposePsResponse:
        """
        Run the docker compose ps command.
        """
        response = rlist()
        for project in projects:
            client = DockerClient(compose_files=project.compose_file_path)
            try:
                containers = client.compose.ps(**cls.FLAGS)
            except DockerException as e:
                raise DockerComposePsError(str(e))

            response.append(
                DockerComposeProjectStatus(
                    project_name=project.name,
                    containers=cls._map_containers(containers),
                )
            )

        return response

    @classmethod
    def _map_containers(cls, containers: list[_Container]) -> rlist[Container]:
        mapped = [
            Container(c.name, cls._map_status(c.state.status)) for c in containers
        ]

        return rlist(mapped)

    @staticmethod
    def _map_status(status: str) -> Status:
        match status:
            case "created":
                return Status.CREATED
            case "running":
                return Status.RUNNING
            case "restarting":
                return Status.RESTARTING
            case "exited":
                return Status.EXITED
            case "paused":
                return Status.PAUSED
            case _:
                return Status.DEAD
