from python_on_whales import DockerClient
from python_on_whales.exceptions import DockerException
from rlist import rlist

from micromanager.models import Project
from micromanager.compose.errors import DockerComposeUpError


class DockerComposeUp:
    """The docker compose up command interface"""

    FLAGS = {
        "detach": True,
        "quiet": False,
    }

    @classmethod
    def call(cls, projects: rlist[Project]) -> None:
        """
        Run the docker compose up command for the given projects.

        Runs compose up on each project separately according to the
        order of the given list.
        """
        for project in projects:
            client = DockerClient(compose_files=project.compose_file_path)
            try:
                client.compose.up(**cls.FLAGS)
            except DockerException as e:
                raise DockerComposeUpError(
                    projects.map(lambda p: p.name).to_list(), str(e)
                ) from None
