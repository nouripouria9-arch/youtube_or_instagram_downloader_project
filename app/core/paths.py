from __future__ import annotations

from pathlib import Path

from app.core.constants import APP_NAME


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = PROJECT_ROOT / "app"
RESOURCES_ROOT = PROJECT_ROOT / "resources"
ICONS_ROOT = RESOURCES_ROOT / "icons"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"


def default_download_dir() -> Path:
    return Path.home() / "Downloads"


def ensure_app_dirs() -> None:
    for directory in (CONFIG_DIR, DATA_DIR, LOG_DIR, default_download_dir()):
        directory.mkdir(parents=True, exist_ok=True)
