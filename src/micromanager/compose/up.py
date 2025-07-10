from python_on_whales import DockerClient

from micromanager.models import Project


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

        docker.compose.up(**cls.FLAGS)
