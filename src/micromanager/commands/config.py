from rich import print

from micromanager.config.app import app_config
from micromanager.commands.app import app


@app.command()
def config() -> None:
    """
    Display the current configuration.
    """
    for name, system in app_config.systems.items():
        print(f"[b bright_green]{name}:[/b bright_green]\n\t{system.pretty_str()}")
