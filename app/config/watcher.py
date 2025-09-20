import threading
from pathlib import Path

from loguru import logger
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from app.config.config import CONFIG_FILE, get_all_settings


class ConfigReloadHandler(FileSystemEventHandler):
    def __init__(self, app, config_path):
        self.app = app
        self.config_path = str(config_path)

    def on_modified(self, event: FileSystemEvent):
        if Path(str(event.src_path)).resolve() == Path(str(self.config_path)).resolve():
            logger.info(f"Config file changed: {self.config_path}, reloading config...")
            self.app.state.config = get_all_settings()


def start_config_watcher(app, config_path=CONFIG_FILE):
    event_handler = ConfigReloadHandler(app, config_path)
    observer = Observer()
    observer.schedule(
        event_handler, path=str(Path(config_path).parent), recursive=False
    )
    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()


def stop_config_watcher(observer):
    """Stop and join the given watchdog observer thread.

    Parameters
    ----------
    observer : Observer
        The watchdog observer instance to stop.
    """
    observer.stop()
    observer.join()
