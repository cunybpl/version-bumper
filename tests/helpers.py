from poetry.poetry import Poetry
from version_bumper.plugin import VersionBumperCommand
from typing import Any


class TestVersionBumperCommand(VersionBumperCommand):
    def __init__(self, poetry: Poetry) -> None:
        super().__init__()
        self._poetry = poetry

    __test__ = False

    def line(self, data: Any):
        print(data)
