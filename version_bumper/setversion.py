#!/usr/bin/env python
""" standalone cli script for easy version bumping with pyproject.
"""
import argparse
import tomllib
import pathlib
import sys
import subprocess


def bash_command(command: str):
    process = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(
            f"{command} failed: {process.returncode} {str(out)} {str(err)}",
            file=sys.stderr,
        )
        sys.exit(2)


def main(package: str, tag: bool = True, push: bool = True):
    # get the pyproject.toml
    try:
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
    except IOError:
        print("pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    version = pyproject["tool"]["poetry"]["version"]

    # set the internal _version.py
    package_root_dir = pathlib.Path(__file__).parent / package
    if not package_root_dir.is_dir():
        print(f"{package} not found", file=sys.stderr)
        sys.exit(1)

    with open(package_root_dir / "_version.py", "w") as f:
        print("#~# generated by setversion.py #~#", file=f)
        print(f'VERSION="{version}" # pragma: no cover', file=f)

    # make a git tag and push
    if tag:
        commit_and_tag = f'git add -A && git commit -m "{version}" && git tag -a {version} -m "{version}"'
        bash_command(commit_and_tag)

        print(f"git tag: {version}")

        if push:
            push_command = f"git push origin {version}"
            bash_command(push_command)
            print(f"git push origin: {version}")


def test_cmd():
    print("This is a test")


if __name__ == "__main__":
    description = """Automatically replaces the internal version with the one in the current pyproject.toml. 
    Optionally will also automatically create a git commit and git tag after versioning.
    """

    parser = argparse.ArgumentParser("setversion", description=description)
    parser.add_argument(
        "package", type=str, help="The package name in this directory to be versioned."
    )

    parser.add_argument(
        "--tag", action="store_true", help="Git commit and tag after setting version."
    )

    parser.add_argument(
        "--push", action="store_true", help="Push the tag to remote origin."
    )

    args = parser.parse_args()

    main(args.package, args.tag, args.push)
