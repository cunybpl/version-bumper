from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin


class CustomCommand(Command):
    name = "test"

    def handle(self) -> int:
        self.line("My command")
        print("My actual command though")
        return 0


def factory() -> "CustomCommand":
    return CustomCommand()


class MyApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("test", factory)
