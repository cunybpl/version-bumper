from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.console.application import Application
from version_bumper.command import VersionBumperCommand


class VersionBumperApplicationPlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        application.command_loader.register_factory(
            VersionBumperCommand.name, lambda: VersionBumperCommand()
        )
