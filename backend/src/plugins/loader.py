import importlib.util
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
PLUGINS_DIR = WORKSPACE_ROOT / 'plugins'


def discover_plugins() -> list[dict[str, Any]]:
    plugins: list[dict[str, Any]] = []

    if not PLUGINS_DIR.exists():
        return plugins

    for plugin_path in PLUGINS_DIR.iterdir():
        if not plugin_path.is_dir():
            continue

        init_file = plugin_path / '__init__.py'
        if not init_file.exists():
            continue

        spec = importlib.util.spec_from_file_location(f'plugins.{plugin_path.name}', init_file)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_obj = getattr(module, 'plugin', None)
        if plugin_obj is None:
            continue

        plugin_name = getattr(plugin_obj, 'get_name', None)
        plugin_version = getattr(plugin_obj, 'get_version', None)
        plugin_enabled = getattr(plugin_obj, 'is_enabled', lambda: True)

        if callable(plugin_name) and callable(plugin_version):
            plugins.append({
                'name': plugin_name(),
                'version': plugin_version(),
                'enabled': plugin_enabled(),
            })

    return plugins
