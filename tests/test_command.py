import pytest
from tests.helpers import TestVersionBumperCommand
from cleo.testers.application_tester import ApplicationTester


def test_command(versionbumper_cmd_tester: TestVersionBumperCommand):
    versionbumper_cmd_tester.handle()


def test_app(test_app: ApplicationTester):
    res = test_app.execute("bumpversion")
    print(res)
