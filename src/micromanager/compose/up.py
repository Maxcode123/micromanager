from python_on_whales import DockerClient

from micromanager.models import Project
from micromanager.compose.errors import DockerComposeUpError


class DockerComposeUp:
    """The docker compose up command interface"""

    FLAGS = {
        "detach": True,
    }

    @classmethod
    def call(cls, projects: list[Project]):
        """
        Run the docker compose up command for the given projects.
        """
        compose_files = list(map(lambda p: str(p.compose_file_path), projects))
        docker = DockerClient(compose_files=compose_files)

        try:
            docker.compose.up(**cls.FLAGS)
        except Exception as e:
            raise DockerComposeUpError(list(map(lambda p: p.name, projects)), str(e))
