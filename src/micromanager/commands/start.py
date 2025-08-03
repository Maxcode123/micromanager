from typing import Annotated

from typer import Argument

from micromanager.models import Project
from micromanager.compose.up import DockerComposeUp
from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.commands.errors import ArgumentValidationError


@app.command()
def start(projects: Annotated[list[str] | None, Argument()] = None) -> None:
    """
    Start the given projects by running compose up.
    If the projects argument is empty, starts all projects of the current system.
    """
    if projects is None:
        _projects = app_config.get_current_system().projects
    else:
        _projects = _parse_input(projects)

    DockerComposeUp.call(_projects)


def _parse_input(projects: list[str]) -> list[Project]:
    current_system = app_config.get_current_system()
    current_project_names = list(map(lambda p: p.name, current_system.projects))

    invalid_input = list(filter(lambda p: p not in current_project_names, projects))
    if len(invalid_input) > 0:
        msg = f"Cannot start projects {invalid_input} as they are not part of the current system '{current_system.name}'.\nAvailable projects: {current_project_names}"
        raise ArgumentValidationError(msg)

    _projects = [p for p in current_system.projects if p.name in projects]
    return _projects
