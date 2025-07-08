from pathlib import Path

from unittest_extensions import TestCase, args

from micromanager.models import System, Project, Service
from micromanager.config.parser import Parser
from micromanager.config.config import AppConfig
from micromanager.tests.unit.mocks import MockParser


class TestAppConfig:
    def parser(self, path=None, json=None, yaml=None):
        path = self.path if path is None else path
        json = self.json if json is None else json
        yaml = self.yaml if yaml is None else yaml
        return Parser(path, MockParser(json), MockParser(yaml))

    def config(self, path=None, json=None, yaml=None):
        return AppConfig(self.parser(path, json, yaml))


class TestAppConfigGetDefaultSystem(TestAppConfig, TestCase):
    def subject(self, path, json, yaml):
        return self.config(path, json, yaml).get_default_system()

    @args(
        path=Path("."),
        json={
            "systems": {
                "mysys": {
                    "projects": {"coolproj": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"app": {}, "db": {}}},
    )
    def test_no_explicit_default_system(self):
        system = System(
            name="mysys",
            is_default=True,
            projects=[
                Project(
                    name="coolproj",
                    compose_file_path=Path("."),
                    services=[Service(name="app"), Service(name="db")],
                )
            ],
        )
        self.assertResult(system)

    @args(
        path=Path("."),
        json={
            "systems": {
                "mysys": {
                    "projects": {"coolproj": {"compose_file_path": "."}},
                },
                "oasys": {
                    "default": True,
                    "projects": {"ecommerce": {"compose_file_path": "."}},
                },
            }
        },
        yaml={"services": {"app": {}, "db": {}}},
    )
    def test_two_systems(self):
        system = System(
            name="oasys",
            is_default=True,
            projects=[
                Project(
                    name="ecommerce",
                    compose_file_path=Path("."),
                    services=[Service(name="app"), Service(name="db")],
                )
            ],
        )
        self.assertResult(system)


class TestAppConfigGetCurrentSystem(TestAppConfig, TestCase):
    def subject(self, path, json, yaml):
        return self.config(path, json, yaml).get_current_system()

    @args(
        path=Path("."),
        json={
            "systems": {
                "mysys": {
                    "projects": {"coolproj": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"app": {}, "db": {}}},
    )
    def test_one_system(self):
        system = System(
            name="mysys",
            is_default=True,
            projects=[
                Project(
                    name="coolproj",
                    compose_file_path=Path("."),
                    services=[Service(name="app"), Service(name="db")],
                )
            ],
        )
        self.assertResult(system)

    @args(
        path=Path("."),
        json={
            "systems": {
                "mysys": {
                    "projects": {"coolproj": {"compose_file_path": "."}},
                },
                "oasys": {
                    "default": True,
                    "projects": {"ecommerce": {"compose_file_path": "."}},
                },
            }
        },
        yaml={"services": {"app": {}, "db": {}}},
    )
    def test_two_systems(self):
        system = System(
            name="oasys",
            is_default=True,
            projects=[
                Project(
                    name="ecommerce",
                    compose_file_path=Path("."),
                    services=[Service(name="app"), Service(name="db")],
                )
            ],
        )
        self.assertResult(system)
