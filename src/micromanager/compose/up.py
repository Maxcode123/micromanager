from typing import Sized

from python_on_whales import DockerClient

from micromanager.models import Project
from micromanager.config.app import app_config


class DockerComposeUp:
    """The docker compose up command interface"""

    FLAGS = {
        "detach": True,
    }

    @classmethod
    def call(cls, projects: Sized[Project] = list()):
        """
        Run the docker compose up command for the given projects.
        """
        if len(projects) == 0:
            projects = app_config.get_current_system().projects

        compose_files = list(map(lambda p: str(p.compose_file_path), projects))
        docker = DockerClient(compose_files=compose_files)

        docker.compose.up(**cls.FLAGS)
