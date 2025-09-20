# ruff: noqa
import pathlib
import threading

from loguru import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from app.config.config import CONFIG_FILE, get_all_settings


def ensure_str_path(path: pathlib.Path | str | bytes) -> str:
    """Ensure the path is returned as a string."""
    if isinstance(path, bytes):
        return path.decode("utf-8")
    return str(path)


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, app, file_path: pathlib.Path, debounce_sec: float = 1.0):  # noqa: ANN001
        self.app = app
        self.file_path = file_path.resolve()
        self.debounce_sec = debounce_sec
        self.debounce_timer: threading.Timer | None = None

    def on_modified(self, event):
        event_path = pathlib.Path(ensure_str_path(event.src_path)).resolve()
        if not getattr(event, "is_directory", False) and event_path == self.file_path:
            logger.info(
                f"Config file change detected. Debouncing for {self.debounce_sec} seconds."
            )
            if self.debounce_timer:
                self.debounce_timer.cancel()
            self.debounce_timer = threading.Timer(
                self.debounce_sec, self._trigger_reload
            )
            self.debounce_timer.start()

    def _trigger_reload(self):
        logger.info("Triggering config reload after debounce.")
        self.app.state.config = get_all_settings()

    def stop(self):
        if self.debounce_timer:
            self.debounce_timer.cancel()
            self.debounce_timer = None


class ConfigFileWatcher:
    def __init__(
        self, app, file_path: pathlib.Path = CONFIG_FILE, debounce_sec: float = 1.0
    ):
        self._observer = Observer()
        self._event_handler = ConfigChangeHandler(app, file_path, debounce_sec)
        self._path_to_watch = file_path.parent

    def start(self):
        self._observer.schedule(
            self._event_handler,
            str(self._path_to_watch),
            recursive=False,
        )
        self._observer.start()
        logger.info(f"Config file watcher started for {self._path_to_watch}")

    def stop(self):
        self._event_handler.stop()
        self._observer.stop()
        self._observer.join()
        logger.info("Config file watcher stopped.")


# Helper to start watcher from FastAPI
def start_config_watcher(app, config_path=CONFIG_FILE, debounce_sec: float = 1.0):
    watcher = ConfigFileWatcher(app, config_path, debounce_sec)
    watcher.start()
    return watcher


# helper to stop watcher from FastAPI
def stop_config_watcher(app):
    if hasattr(app, "state") and hasattr(app.state, "config_watcher"):
        watcher = app.state.config_watcher
        if watcher:
            watcher.stop()
            app.state.config_watcher = None
            logger.info("Config watcher stopped from FastAPI.")
