from rlist import rlist

from micromanager.config.app import app_config
from micromanager.models import Project
from micromanager.commands.errors import ArgumentValidationError


def parse_projects(projects: list[str]) -> list[Project]:
    """
    Parses a list of strings into Project models.
    Raises ArgumentValidationError if a project is not in the current system.
    """
    current_system = app_config.get_current_system()
    current_project_names = rlist(current_system.projects).map(lambda p: p.name)

    invalid_input = rlist(projects).select(lambda p: p not in current_project_names)
    if len(invalid_input) > 0:
        msg = f"Cannot start projects {invalid_input} as they are not part of the current system '{current_system.name}'.\nAvailable projects: {current_project_names}"
        raise ArgumentValidationError(msg)

    _projects = [p for p in current_system.projects if p.name in projects]
    return _projects


def get_project_names() -> rlist[str]:
    """
    Get the names of the projects in the current system.
    """
    return app_config.get_current_system().projects.map(lambda p: p.name)
