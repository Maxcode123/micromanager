from pathlib import Path


class MockParser:
    def __init__(self, parsed_content: dict) -> None:
        self.parsed_content = parsed_content

    def load(self, path: Path) -> dict:
        return self.parsed_content
