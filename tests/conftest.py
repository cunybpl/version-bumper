import pytest
from pathlib import Path
from cleo.testers.application_tester import ApplicationTester
from poetry.factory import Factory
from tests.helpers import TestApplication, TestVersionBumperCommand
from poetry.poetry import Poetry
from version_bumper.command import VersionBumperCommand


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
