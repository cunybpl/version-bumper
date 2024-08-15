from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin

PLUGIN_NAME = "test"


class CustomCommand(Command):
    name = PLUGIN_NAME

    def handle(self) -> int:
        print("My actual command though")
        return 0


def factory() -> "CustomCommand":
    return CustomCommand()


class MyApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory(PLUGIN_NAME, factory)
