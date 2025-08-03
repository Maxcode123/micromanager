lint:
	ruff check

lint-imports:
	uv run lint-imports --verbose --config src/micromanager/.importlinter

format:
	ruff format ./

type-check:
	uv run ty check

test:
	uv run python -m unittest discover -v src/micromanager/tests/unit

install-local-package:
	uv pip install -e .

build:
	uv build

start:
	uv run typer src/micromanager/main.py run start

stop:
	uv run typer src/micromanager/main.py run stop

help:
	uv run typer src/micromanager/main.py run --help
