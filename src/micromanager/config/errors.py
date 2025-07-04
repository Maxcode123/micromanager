class ParserError(Exception):
    """Base class for errors originating in the configuration parser."""

    pass


class InvalidConfigFileError(ParserError):
    """The configuration file is invalid, e.g. because of a typo."""

    def __init__(self, path: str, error: str) -> None:
        msg = f"The micromanager configuration file {path} is invalid: {error}"
        super().__init__(msg)


class ConfigFileDoesNotExistError(ParserError):
    """The micromanager configuration file was not found in the predefined paths."""

    def __init__(self, paths: list[str]) -> None:
        msg = f"The micromanager configuration file was not found in the predefined paths: {paths}"
        super().__init__(msg)


class ComposeFileDoesNotExistError(ParserError):
    """A compose file was not found in the given path."""

    def __init__(self, project_name: str, path: str) -> None:
        msg = f"The compose_file_path field of the project {project_name} does not point to an existing path {path}"
        super().__init__(msg)
