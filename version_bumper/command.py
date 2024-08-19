from poetry.console.commands.version import Command as VersionCommand
from poetry.console.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from cleo.helpers import argument
from cleo.helpers import option
from enum import Enum


class VersionRule(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"


def factory() -> "VersionBumperCommand":
    return VersionBumperCommand


class VersionBumperCommand(Command):
    name = "bumpversion"
    description = "Bumps a project's version."

    # arguments: list[Argument] = [
    #     argument(
    #         "version",
    #         "The version number or the rule to update the version.",
    #         optional=False,
    #     ),
    #     argument(
    #         "module-name",
    #         "The module name to bump.",
    #         optional=False,
    #     ),
    # ]

    # options: list[Option] = [
    #     option("tag", "Whether to create a tag or not. (?)", flag=True),
    #     option("push", "Whether to push that tag or not. (?)", flag=True),
    #     option("dry-run", "Whether to actually make changes or not", flag=True),
    # ]

    def handle(self) -> int:
        # version = self.argument("version")
        # module_name = self.argument("module-name")
        # tag = self.option("tag")
        # push = self.option("push")
        # dry_run = self.option("dry-run")

        # version = "prerelease"

        # new_version = self.increment_version(
        #     self.poetry.package.pretty_version, version
        # )

        print("This is the custom command")
        return 0
