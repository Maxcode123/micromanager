from typing import Annotated

from typer import Argument
from rich import print

from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.commands.errors import ArgumentValidationError


def _autocompletion(incomplete: str):
    names = app_config.systems.keys()
    for name in names:
        if name.startswith(incomplete):
            yield name


@app.command()
def use(system: Annotated[str, Argument(autocompletion=_autocompletion)]) -> None:
    """
    Set the given system as your current working system.
    """
    s = app_config.systems.get(system, None)
    if s is None:
        available_systems = list(app_config.systems.keys())
        raise ArgumentValidationError(
            f"system {system} is not found in the configured systems; check {app_config.config_file_path()}\nAvailable systems: {available_systems}"
        )

    app_config.set_current_system(s)
    print(f"Using system: {s.name}")
