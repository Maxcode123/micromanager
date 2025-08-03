from typing import Annotated

from typer import Argument
from rlist import rlist

from micromanager.models import Project
from micromanager.compose.down import DockerComposeDown
from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.commands.errors import ArgumentValidationError
from micromanager.commands.utils import parse_projects


@app.command()
def stop(projects: Annotated[list[str] | None, Argument()] = None) -> None:
    """
    Stop the given projects by running compose down.
    If the projects argument is empty, stops all projects of the current system.
    """
    if projects is None:
        _projects = app_config.get_current_system().projects
    else:
        _projects = parse_projects(projects)

    DockerComposeDown.call(rlist(_projects))
