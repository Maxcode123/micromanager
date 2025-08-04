from python_on_whales import DockerClient
from python_on_whales.exceptions import DockerException
from rlist import rlist

from micromanager.models import Project
from micromanager.compose.errors import DockerComposeDownError


class DockerComposeDown:
    """The docker compose down command interface"""

    FLAGS = {
        "quiet": False,
    }

    @classmethod
    def call(cls, projects: rlist[Project]):
        """
        Run the docker compose down command for the given projects.
        """
        compose_files = projects.map(lambda p: str(p.compose_file_path))
        docker = DockerClient(compose_files=compose_files.to_list())

        try:
            docker.compose.down(**cls.FLAGS)
        except DockerException as e:
            raise DockerComposeDownError(
                projects.map(lambda p: p.name).to_list(), str(e)
            ) from None
