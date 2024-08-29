from poetry.console.commands.version import VersionCommand
from poetry.core.constraints.version import Version
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from cleo.helpers import argument
from cleo.helpers import option
from typing import Any
import subprocess
import pathlib


class VersionBumperCommand(VersionCommand):
    name = "bumpversion"
    description = "Bumps a project's version."

    arguments: list[Argument] = [  # type: ignore
        argument(
            "version",
            "The version number or the rule to update the version.",
            optional=False,
        ),
        argument(
            "module-name",
            "The module name to bump.",
            optional=False,
        ),
    ]

    options: list[Option] = [  # type: ignore
        option(
            "tag",
            "-t",
            "Create a new tag",
            flag=True,
            value_required=False,
        ),
        option(
            "push",
            "-p",
            "Push the tag",
            flag=True,
            value_required=False,
        ),
        option(
            "dry-run",
            "-d",
            flag=True,
            value_required=False,
        ),
    ]

    help = """
The version command bumps the version of the project and writes 
the new version back to pyproject.toml and <module>/_version.py 
if a valid bump rule is provided.

The new version should ideally be a valid semver string or a valid bump rule:
patch, minor, major, prepatch, preminor, premajor, prerelease.
    """

    def handle(self) -> int:
        version = self.argument("version")
        module_name = self.argument("module-name")
        tag = self.option("tag")
        push = self.option("push")
        dry_run = self.option("dry-run")

        module_path: pathlib.Path = (
            pathlib.Path(str(self.poetry.file)).parent / module_name
        )
        if not module_path.is_dir():
            self.line_error(f"Could not find module {module_name} ({module_path})")
            return 1

        new_version = self.increment_version(
            self.poetry.package.pretty_version, version
        )
        self.line(
            f"Bumping {module_name} from {self.poetry.package.pretty_version} -> {new_version} ({version})"
        )

        if not dry_run:
            self.line("Bumping version in pyproject.toml...")
            self._write_new_version(new_version)

            self.line(f"Bumping {module_name}/_version.py file...")
            self._write_new_version_file(
                module_path=module_path, new_version=new_version
            )

            if tag:
                self.line("Creating tag...")
                result = self._create_tag(tag_version=new_version)
                if result != 0:
                    self.line_error("There was an error creating the tag")
                    return result

                if push:
                    self.line("Pushing tag...")
                    result = self._push_tag(tag_version=new_version)
                    if result != 0:
                        self.line_error("There was an error pushing the tag")
                        return result
        else:
            self.line("Dry run.")

        return 0

    def _bash_command(self, command: str) -> int:
        process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            self.line_error(
                f"{command} failed: {process.returncode} {str(out)} {str(err)}"
            )
        return process.returncode

    def _write_new_version(self, new_version: Version) -> None:
        content: dict[str, Any] = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        poetry_content["version"] = str(new_version)
        self.poetry.file.write(content)  # type: ignore

    def _write_new_version_file(
        self, module_path: pathlib.Path, new_version: Version
    ) -> None:
        with open(module_path / "_version.py", "w") as _version:
            print("#~# generated by poetry bumpversion #~#", file=_version)
            print(f'VERSION="{new_version}" # pragma: no cover', file=_version)

    def _create_tag(self, tag_version: Version) -> int:
        return self._bash_command(
            f'git add -A && git commit -m "{tag_version}" && git tag -a {tag_version} -m "{tag_version}"'
        )

    def _push_tag(self, tag_version: Version) -> int:
        return self._bash_command(f"git push origin {tag_version}")
