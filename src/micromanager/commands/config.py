from rich import print

from micromanager.models import System, Project
from micromanager.config.app import app_config
from micromanager.commands.app import app


@app.command()
def config() -> None:
    """
    Display the current configuration.
    """
    print(f"micromanager configuration file: {app_config.config_file_path()}")
    for name, system in app_config.systems.items():
        print(
            f"[b bright_green]{name}:[/b bright_green]\n\t{system_pretty_str(system)}"
        )


def system_pretty_str(system: System) -> str:
    """
    Return a pretty-formatted string representation of a System.
    """
    s = f"""name: {system.name}
        is_default: {system.is_default}
        projects:"""
    s += "\n"
    for project in system.projects:
        s += "\t\t" + project_pretty_str(project)

    return s


def project_pretty_str(project: Project) -> str:
    """
    Return a pretty-formatted string representation of a Project.
    """
    s = f"""name: {project.name}
                compose_file_path: {project.compose_file_path}
                services:"""
    s += "\n"
    for service in project.services:
        s += "\t\t\t" + service.name + "\n"

    return s
