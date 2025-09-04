lint:
	ruff check

lint-imports:
	uv run lint-imports --verbose --config src/micromanager/.importlinter

format:
	ruff format ./

type-check:
	uv run ty check --exclude src/micromanager/tests/

test:
	uv run python -m unittest discover -v src/micromanager/tests/unit

test-integration:
	uv run python -m unittest discover -v src/micromanager/tests/integration

install-local-package:
	uv pip install -e .

build:
	uv build

publish:
	uv publish

clean:
	rm -rf dist/
	rm -rf src/compose_micromanager.egg-info/
	rm -rf src/micromanager.egg-info

start:
	uv run typer src/micromanager/main.py run start

stop:
	uv run typer src/micromanager/main.py run stop

status:
	uv run typer src/micromanager/main.py run status

help:
	uv run typer src/micromanager/main.py run --help

start-documentation-server:
	uv run python -m mkdocs serve

deploy-documentation:
	uv run python -m mkdocs gh-deploy --config-file mkdocs.yml
