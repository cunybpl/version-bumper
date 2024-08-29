import pytest
from version_bumper.command import VersionBumperCommand


def test_increment_version(command_instance: VersionBumperCommand):
    cmd = VersionBumperCommand()

    assert str(cmd.increment_version("0.1.0", "minor")) == "0.2.0"
    assert str(cmd.increment_version("0.1.0", "prerelease")) == "0.1.1a0"
    assert str(cmd.increment_version("0.1.0", "major")) == "1.0.0"
    assert str(cmd.increment_version("0.1.0", "patch")) == "0.1.1"

    with pytest.raises(ValueError):
        cmd.increment_version("abc123", "minor")

    with pytest.raises(ValueError):
        cmd.increment_version("0.1.0", "abc123")
