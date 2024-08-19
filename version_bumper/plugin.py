from poetry.plugins.application_plugin import ApplicationPlugin
from version_bumper.command import VersionBumperCommand, factory


class VersionBumperApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory(VersionBumperCommand.name, factory)
