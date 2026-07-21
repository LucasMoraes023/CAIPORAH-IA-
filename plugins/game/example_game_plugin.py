from src.plugins.plugin_base import PluginBase

class GamePlugin(PluginBase):
    def get_name(self) -> str:
        return 'Example Game Plugin'

    def get_version(self) -> str:
        return '0.1.0'

    def activate(self) -> None:
        pass

    def deactivate(self) -> None:
        pass

    def is_enabled(self) -> bool:
        return True
