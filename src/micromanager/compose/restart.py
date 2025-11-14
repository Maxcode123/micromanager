from python_on_whales import DockerClient
from python_on_whales.exceptions import DockerException
from rlist import rlist

from micromanager.models import Project
from micromanager.compose.errors import DockerComposeRestartError


class DockerComposeRestart:
    """The docker compose up command interface"""

    @classmethod
    def call(cls, projects: rlist[Project]) -> None:
        """
        Run the docker compose restart command for the given projects.

        Runs compose restart on each project separately according to the
        order of the given list.
        """
        for project in projects:
            client = DockerClient(compose_files=project.compose_file_path)
            try:
                client.compose.restart()
            except DockerException as e:
                raise DockerComposeRestartError(
                    projects.map(lambda p: p.name).to_list(), str(e)
                ) from None
