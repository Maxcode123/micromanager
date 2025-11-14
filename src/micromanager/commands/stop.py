from typing import Annotated

from typer import Argument
from rlist import rlist
from rich import print

from micromanager.compose.down import DockerComposeDown
from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.commands.utils import parse_projects, get_project_names


def _autocompletion(incomplete: str):
    for name in get_project_names():
        if name.startswith(incomplete):
            yield name


@app.command()
def stop(
    projects: Annotated[
        list[str] | None, Argument(autocompletion=_autocompletion)
    ] = None,
) -> None:
    """
    Stop the given projects by running compose down.
    If the projects argument is empty, stops all projects of the current system.
    """
    if projects is None:
        _projects = app_config.get_current_system().projects
    else:
        _projects = parse_projects(projects)

    _projects = rlist(_projects)
    DockerComposeDown.call(rlist(_projects))
    print(f"Stopped projects: {_projects.map(lambda p: p.name).to_list()}")
