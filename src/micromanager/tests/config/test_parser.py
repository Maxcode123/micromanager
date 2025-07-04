from pathlib import Path

from unittest_extensions import TestCase, args

from micromanager.models import System, Project, Service
from micromanager.config.parser import Parser
from micromanager.config.errors import (
    ConfigFileDoesNotExistError,
    ComposeFileDoesNotExistError,
    InvalidConfigFileError,
)
from micromanager.tests.mocks import MockParser


class TestParser(TestCase):
    def parser(self, paths=None, json=None, yaml=None):
        paths = self.paths if paths is None else paths
        json = self.json if json is None else json
        yaml = self.yaml if yaml is None else yaml
        return Parser(paths, MockParser(json), MockParser(yaml))

    def subject(self, paths=None, json=None, yaml=None):
        return self.parser(paths, json, yaml).parse()

    def assert_invalid_config(self):
        self.assertResultRaises(InvalidConfigFileError)

    @args(
        paths=[Path(".")],
        json={
            "systems": {
                "mysys": {
                    "default": True,
                    "projects": {"coolproj": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"db": {}, "backend": {}, "frontend": {}}},
    )
    def test_parse_one_default_system(self):
        system = System(
            name="mysys",
            is_default=True,
            projects=[
                Project(
                    name="coolproj",
                    compose_file_path=Path("."),
                    services=[
                        Service(name="db"),
                        Service(name="backend"),
                        Service(name="frontend"),
                    ],
                )
            ],
        )
        self.assertResultDict({"mysys": system})

    @args(
        paths=[Path(".")],
        json={
            "systems": {
                "sysy": {"projects": {"ecommerce": {"compose_file_path": ".."}}},
                "systa": {
                    "default": True,
                    "projects": {"shipping": {"compose_file_path": ".."}},
                },
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_two_systems(self):
        sysy = System(
            name="sysy",
            is_default=False,
            projects=[
                Project(
                    name="ecommerce",
                    compose_file_path=Path(".."),
                    services=[Service(name="app")],
                )
            ],
        )
        systa = System(
            name="systa",
            is_default=True,
            projects=[
                Project(
                    name="shipping",
                    compose_file_path=Path(".."),
                    services=[Service(name="app")],
                )
            ],
        )
        self.assertResultDict({"sysy": sysy, "systa": systa})

    @args(
        paths=[Path(".")],
        json={
            "systems": {
                "sys": {
                    "default": True,
                    "projects": {
                        "ecommerce": {"compose_file_path": "."},
                        "payments": {"compose_file_path": "."},
                    },
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_multiple_projects(self):
        system = System(
            name="sys",
            is_default=True,
            projects=[
                Project(
                    name="ecommerce",
                    compose_file_path=Path("."),
                    services=[Service(name="app")],
                ),
                Project(
                    name="payments",
                    compose_file_path=Path("."),
                    services=[Service(name="app")],
                ),
            ],
        )
        self.assertResultDict({"sys": system})

    @args(
        paths=[Path("some/path/muhahaha")],
        json={
            "systems": {
                "sys": {
                    "default": True,
                    "projects": {"ecommerce": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_nonexisting_path(self):
        self.assertResultRaises(ConfigFileDoesNotExistError)

    @args(
        paths=[Path("some/path/muhahaha"), Path(".")],
        json={
            "systems": {
                "sys": {
                    "default": True,
                    "projects": {"ecommerce": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_existing_and_nonexisting_path(self):
        self.assertResultNotRaises()

    @args(
        paths=[Path(".")],
        json={
            "systems": {
                "sys": {
                    "projects": {"ecommerce": {"compose_file_path": "."}},
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_default_key_missing_from_single_system(self):
        self.assertResultNotRaises()

    @args(
        paths=[Path(".")],
        json={
            "systems": {
                "sys": {
                    "projects": {
                        "ecommerce": {"compose_file_path": "some/path/to/somewhere"}
                    },
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_nonexisting_compose_file_path(self):
        self.assertResultRaises(ComposeFileDoesNotExistError)

    @args(
        paths=[Path(".")],
        json={
            "systemsssss": {
                "sys": {
                    "projects": {
                        "ecommerce": {"compose_file_path": "some/path/to/somewhere"}
                    },
                }
            }
        },
        yaml={"services": {"app": {}}},
    )
    def test_parse_invalid_configuration_systems_field(self):
        self.assert_invalid_config()

    @args(
        paths=[Path(".")],
        json={"systems": object()},
        yaml={"services": {"app": {}}},
    )
    def test_parse_invalid_configuration_systems_value(self):
        self.assert_invalid_config()

    @args(
        paths=[Path(".")],
        json={"systems": {"sys": {"projectssss": {}}}},
        yaml={"services": {"app": {}}},
    )
    def test_parse_invalid_configuration_projects_field(self):
        self.assert_invalid_config()
