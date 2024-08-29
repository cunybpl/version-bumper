import pytest
from pathlib import Path
from cleo.testers.application_tester import ApplicationTester
from poetry.factory import Factory
from tests.helpers import TestApplication, TestVersionBumperCommand
from poetry.poetry import Poetry
from typing import Any


@pytest.fixture
def simple_project_path() -> Path:
    return Path(__file__).parent / "fixtures" / "simple_project"


@pytest.fixture
def test_app(simple_project_path: Path):
    poetry = Factory().create_poetry(simple_project_path)
    app = TestApplication(poetry)
    return ApplicationTester(app)


@pytest.fixture
def poetry(simple_project_path: Path) -> Poetry:
    return Factory().create_poetry(simple_project_path)


@pytest.fixture
def versionbumper_cmd_tester(poetry: Poetry) -> TestVersionBumperCommand:
    return TestVersionBumperCommand(poetry)


@pytest.fixture
def expected_pyproj_content() -> dict[str, Any]:
    return {
        "tool": {
            "poetry": {
                "name": "simpleproj",
                "version": "1.0.0",
                "description": "",
                "authors": ["Kuba Gasiorowski <kgasiorowski123@gmail.com>"],
                "readme": "README.md",
                "dependencies": {"python": "^3.11", "poetry": "^1.8.3"},
            }
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        },
    }
