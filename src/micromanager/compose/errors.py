class DockerComposeError(Exception):
    """
    An error occured on the execution of a docker compose command.
    """


class DockerComposeUpError(DockerComposeError):
    """
    An error occured on the execution of docker compose up.
    """

    def __init__(self, projects: list[str], error: str) -> None:
        msg = (
            "An error occured during the execution of docker compose up for the"
            + f" projects {projects}: {error}"
        )
        super().__init__(msg)


class DockerComposeDownError(DockerComposeError):
    """
    An error occured on the execution of docker compose down.
    """

    def __init__(self, projects: list[str], error: str) -> None:
        msg = f"An error occured during the execution of docker compose down for the projects {projects}: {error}"
        super().__init__(msg)


class DockerComposePsError(DockerComposeError):
    """
    An error occured on the execution of docker compose ps.
    """
