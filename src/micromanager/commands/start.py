from typing import Annotated

from typer import Argument
from rlist import rlist
from rich import print

from micromanager.compose.up import DockerComposeUp
from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.commands.utils import parse_projects


@app.command()
def start(projects: Annotated[list[str] | None, Argument()] = None) -> None:
    """
    Start the given projects by running compose up.
    If the projects argument is empty, starts all projects of the current system.
    """
    if projects is None:
        _projects = app_config.get_current_system().projects
    else:
        _projects = parse_projects(projects)

    _projects = rlist(_projects)
    DockerComposeUp.call(_projects)
    print(f"Started projects: {_projects.map(lambda p: p.name).to_list()}")
