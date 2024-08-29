import pytest
from tests.helpers import TestVersionBumperCommand
from pytest_mock import MockerFixture
from pathlib import Path
from version_bumper.command import VersionBumperCommand


def test_increment_version(versionbumper_cmd_tester: TestVersionBumperCommand):
    cmd = versionbumper_cmd_tester

    assert str(cmd.increment_version("0.1.0", "minor")) == "0.2.0"
    assert str(cmd.increment_version("0.1.0", "prerelease")) == "0.1.1a0"
    assert str(cmd.increment_version("0.1.0", "major")) == "1.0.0"
    assert str(cmd.increment_version("0.1.0", "patch")) == "0.1.1"

    with pytest.raises(ValueError):
        cmd.increment_version("abc123", "minor")

    with pytest.raises(ValueError):
        cmd.increment_version("0.1.0", "abc123")


def test_create_tag(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester
    mocked = mocker.patch(
        "version_bumper.command.VersionBumperCommand._bash_command", return_value=0
    )
    assert cmd._create_tag("test") == 0
    mocked.assert_called_once_with(
        'git add -A && git commit -m "test" && git tag -a test -m "test"'
    )


def test_push_tag(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester
    mocked = mocker.patch(
        "version_bumper.command.VersionBumperCommand._bash_command", return_value=0
    )
    assert cmd._push_tag("test") == 0
    mocked.assert_called_once_with("git push origin test")


def test_write_new_version(
    mocker: MockerFixture,
    versionbumper_cmd_tester: TestVersionBumperCommand,
    expected_pyproj_content,
):
    cmd = versionbumper_cmd_tester
    mocked = mocker.patch("tomlkit.toml_file.TOMLFile.write")
    cmd._write_new_version("1.0.0")
    mocked.assert_called_once_with(expected_pyproj_content)


def test_write_version_file(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    version_file_patch = mocker.patch("builtins.open", mocker.mock_open())
    versionbumper_cmd_tester._write_new_version_file(Path("fake/path/"), "1.0.0")
    version_file = version_file_patch()
    version_file.write.assert_called_once_with(
        '#~# generated by poetry bumpversion #~#\nVERSION="1.0.0" # pragma: no cover'
    )


def test_handle_dry_run(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester

    # Provide args and options
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.argument",
        side_effect=["prerelease", "simpleproj"],
    )
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.option",
        side_effect=[True, True, True],  # Dry run true
    )

    # Patch our helper functions
    pyproj_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version"
    )
    versionpy_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version_file"
    )
    createtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._create_tag", return_value=0
    )
    pushtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._push_tag", return_value=0
    )

    assert cmd.handle() == 0

    pyproj_patch.assert_not_called()
    versionpy_patch.assert_not_called()
    createtag_patch.assert_not_called()
    pushtag_patch.assert_not_called()


def test_handle_create_tag(
    mocker: MockerFixture,
    versionbumper_cmd_tester: TestVersionBumperCommand,
):
    cmd = versionbumper_cmd_tester

    # Provide args and options
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.argument",
        side_effect=["prerelease", "simpleproj"],
    )
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.option",
        side_effect=[True, False, False],  # Create tag, but do not push
    )

    # Patch our helper functions
    pyproj_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version"
    )
    versionpy_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version_file"
    )
    createtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._create_tag", return_value=0
    )
    pushtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._push_tag", return_value=0
    )

    assert cmd.handle() == 0

    pyproj_patch.assert_called_once()
    versionpy_patch.assert_called_once()
    createtag_patch.assert_called_once()
    pushtag_patch.assert_not_called()


def test_handle_create_tag_and_push(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester

    # Provide args and options
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.argument",
        side_effect=["prerelease", "simpleproj"],
    )
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.option",
        side_effect=[True, True, False],  # Create tag and push it
    )

    # Patch our helper functions
    pyproj_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version"
    )
    versionpy_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version_file"
    )
    createtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._create_tag", return_value=0
    )
    pushtag_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._push_tag", return_value=0
    )

    assert cmd.handle() == 0

    pyproj_patch.assert_called_once()
    versionpy_patch.assert_called_once()
    createtag_patch.assert_called_once()
    pushtag_patch.assert_called_once()


def test_handle_bash_tag_create_fail(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester

    # Provide args and options
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.argument",
        side_effect=["prerelease", "simpleproj"],
    )
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.option",
        side_effect=[True, True, False],  # Create tag and push it
    )

    # Patch our helper functions
    pyproj_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version"
    )
    versionpy_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version_file"
    )
    mocker.patch("version_bumper.command.VersionBumperCommand.line_error")

    # A bash command failed
    bash_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._bash_command", return_value=1
    )

    create_tag_spy = mocker.spy(VersionBumperCommand, "_create_tag")
    push_tag_spy = mocker.spy(VersionBumperCommand, "_push_tag")

    assert cmd.handle() != 0

    bash_patch.assert_called_once()
    pyproj_patch.assert_called_once()
    versionpy_patch.assert_called_once()
    create_tag_spy.assert_called_once()
    push_tag_spy.assert_not_called()


def test_handle_bash_tag_push_fail(
    mocker: MockerFixture, versionbumper_cmd_tester: TestVersionBumperCommand
):
    cmd = versionbumper_cmd_tester

    # Provide args and options
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.argument",
        side_effect=["prerelease", "simpleproj"],
    )
    mocker.patch(
        "version_bumper.command.VersionBumperCommand.option",
        side_effect=[True, True, False],  # Create tag and push it
    )

    # Patch our helper functions
    pyproj_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version"
    )
    versionpy_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._write_new_version_file"
    )
    mocker.patch("version_bumper.command.VersionBumperCommand.line_error")

    createtag_spy = mocker.spy(VersionBumperCommand, "_create_tag")
    pushtag_spy = mocker.spy(VersionBumperCommand, "_push_tag")

    # A bash command failed
    bash_patch = mocker.patch(
        "version_bumper.command.VersionBumperCommand._bash_command", side_effect=[0, 1]
    )

    assert cmd.handle() != 0

    assert bash_patch.call_count == 2
    pyproj_patch.assert_called_once()
    versionpy_patch.assert_called_once()
    createtag_spy.assert_called_once()
    pushtag_spy.assert_called_once()
