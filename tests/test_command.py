import pytest
from version_bumper.command import VersionBumperCommand
from poetry.poetry import Poetry


def test_increment_version():
    cmd = VersionBumperCommand()

    assert str(cmd.increment_version("0.1.0", "minor")) == "0.2.0"
    assert str(cmd.increment_version("0.1.0", "prerelease")) == "0.1.1a0"
    assert str(cmd.increment_version("0.1.0", "major")) == "1.0.0"
    assert str(cmd.increment_version("0.1.0", "patch")) == "0.1.1"

    with pytest.raises(ValueError):
        cmd.increment_version("abc123", "minor")

    with pytest.raises(ValueError):
        cmd.increment_version("0.1.0", "abc123")


def test_poetry(poetry: Poetry):
    print(poetry.file)
