class MockParser:
    def __init__(self, parsed_content):
        self.parsed_content = parsed_content

    def load(self, *_args, **_kwargs):
        return self.parsed_content
