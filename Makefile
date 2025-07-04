format:
	ruff format ./


test:
	uv run python -m unittest discover -v src/micromanager/tests/


install-local-package:
	uv pip install -e .
