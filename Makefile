lint:
	ruff check

format:
	ruff format ./

type-check:
	uv run ty check

test:
	uv run python -m unittest discover -v src/micromanager/tests/unit

install-local-package:
	uv pip install -e .

run:
	uv run typer src/micromanager/main.py run
