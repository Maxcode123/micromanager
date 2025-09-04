from typing import Generator
from collections import Counter

from rich import print

from micromanager.config.app import app_config
from micromanager.commands.app import app
from micromanager.compose.ps import DockerComposePs, DockerComposePsResponse


@app.command()
def status() -> None:
    """
    Print the status of all configured projects in the current system.
    """
    response = DockerComposePs.call(app_config.get_current_system().projects)

    table = StatusTable(response)
    print(table.format())


class StatusTable:
    HEADERS = ("PROJECT", "STATUS")
    ROW_LENGTHS = (25,)

    def __init__(self, response: DockerComposePsResponse) -> None:
        self._response = response

    def format(self) -> str:
        table = self._format_headers() + "\n"
        table_len = len(self._response)
        for i, row in enumerate(self._rows()):
            table += self._format_row(row)

            if i != table_len - 1:
                table += "\n"

        return table

    def _format_headers(self) -> str:
        headers = self.HEADERS[0]
        headers += self._whitespace(self.HEADERS[0])
        headers += self.HEADERS[1]

        return headers

    def _format_row(self, row: tuple[str, str]) -> str:
        _row = row[0]
        _row += self._whitespace(row[0])
        _row += row[1]
        return _row

    def _whitespace(self, value: str) -> str:
        return " " * self._whitespace_chars(value)

    def _whitespace_chars(self, value: str) -> int:
        return self.ROW_LENGTHS[0] - len(value)

    def _rows(self) -> Generator[tuple[str, str]]:
        for project in self._response:
            if len(project.containers) == 0:
                status = "STOPPED"
            else:
                stata = Counter(project.containers.map(lambda c: c.status))

                status = stata.most_common(1)[0][0]
                in_status = stata[status]
                fraction = "(" + str(in_status) + "/" + str(stata.total()) + ")"

                status = status.value + " " + fraction

            yield (project.project_name, status)
