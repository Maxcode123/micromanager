lint:
	ruff check

format:
	ruff format ./


test:
	uv run python -m unittest discover -v src/micromanager/tests/unit


install-local-package:
	uv pip install -e .
