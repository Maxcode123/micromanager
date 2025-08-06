.PHONY: install-uv
install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: install-linter
install-linter:
	curl -LsSf https://astral.sh/ruff/install.sh | sh

.PHONY: install-type-checker
install-type-checker:
	uv add --dev ty

.PHONY: install-import-linter
install-import-linter:
	uv add --dev import-linter

.PHONY: lint
lint:
	ruff check

.PHONY: lint-imports
lint-imports:
	uv run lint-imports --verbose --config src/micromanager/.importlinter

.PHONY: format
format:
	ruff format ./

.PHONY: type-check
type-check:
	uv run ty check --exclude src/micromanager/tests/

.PHONY: test
test:
	uv run python -m unittest discover -v src/micromanager/tests/unit

.PHONY: test-integration
test-integration:
	uv run python -m unittest discover -v src/micromanager/tests/integration

.PHONY: install-local-package
install-local-package:
	uv pip install -e .

.PHONY: build
build:
	uv build

.PHONY: publish
publish:
	uv publish

.PHONY: clean
clean:
	rm -rf dist/
	rm -rf src/compose_micromanager.egg-info/
	rm -rf src/micromanager.egg-info

.PHONY: start
start:
	uv run typer src/micromanager/main.py run start

.PHONY: stop
stop:
	uv run typer src/micromanager/main.py run stop

.PHONY: status
status:
	uv run typer src/micromanager/main.py run status

.PHONY: help
help:
	uv run typer src/micromanager/main.py run --help

.PHONY: start-documentation-server
start-documentation-server:
	uv run python -m mkdocs serve

.PHONY: deploy-documentation
deploy-documentation:
	uv run python -m mkdocs gh-deploy --config-file mkdocs.yml
