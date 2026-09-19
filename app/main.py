from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QInputDialog

from app.core.config import AppSettings
from app.core.logger import build_logger
from app.core.paths import ensure_app_dirs
from app.core.constants import INSTAGRAM_PLATFORM, YOUTUBE_PLATFORM
from app.ui.main_window import MainWindow
from app.ui.styles.theme import apply_palette

logger = build_logger("app.main")


def boot_app() -> None:
    ensure_app_dirs()
    settings = AppSettings.load()
    app = QApplication(sys.argv)
    app.setApplicationName("Professional YouTube Downloader")
    app.setOrganizationName("ProfessionalApps")
    app.setWindowIcon(QIcon(str(Path(__file__).resolve().parents[1] / "resources" / "icons" / "app_icon.ico")))
    apply_palette(app, settings.theme)
    platform, accepted = QInputDialog.getItem(
        None,
        "Choose downloader",
        "Select the downloader you want to use:",
        ["YouTube Downloader", "Instagram Downloader"],
        0,
        False,
    )
    if not accepted:
        return
    selected_platform = INSTAGRAM_PLATFORM if platform.startswith("Instagram") else YOUTUBE_PLATFORM
    window = MainWindow(settings, selected_platform)
    window.show()
    logger.info("Application initialized")
    sys.exit(app.exec())


if __name__ == "__main__":
    boot_app()
