import os
from contextlib import contextmanager

from typer.testing import CliRunner
from rlist import rlist


runner = CliRunner()


@contextmanager
def test_app(compose_teardown):
    os.environ["MICROMANAGER_CONFIG_PATH"] = (
        "$MICROMANAGER_ROOT/src/micromanager/tests/integration/files/configs/config.json"
    )
    from micromanager.main import app
    from micromanager.config.app import app_config
    from micromanager.compose.down import DockerComposeDown

    try:
        yield app
    finally:
        del os.environ["MICROMANAGER_CONFIG_PATH"]

        if compose_teardown:
            projects = app_config.get_current_system().projects
            DockerComposeDown.call(rlist(projects))


def run(args: str | list[str], *, compose_teardown=True):
    with test_app(compose_teardown) as app:
        return runner.invoke(app, args)
