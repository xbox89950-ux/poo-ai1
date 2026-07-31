"""Simple plugin manager"""
import importlib.util
import logging
from config.settings import SETTINGS

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        plugins_dir = SETTINGS.PLUGINS_DIR
        if not plugins_dir.exists():
            return
        for file in plugins_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(file.stem, file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "register"):
                    self.plugins[file.stem] = mod
                    logger.info(f"Loaded plugin: {file.stem}")
            except Exception as e:
                logger.error(f"Failed to load plugin {file}: {e}")

    def run_plugin(self, name: str, *args, **kwargs):
        if name in self.plugins:
            return self.plugins[name].register(*args, **kwargs)
        return None
