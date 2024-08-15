import pytest
from version_bumper import plugin


def test_command():
    cmd = plugin.CustomCommand()
    cmd.handle()
