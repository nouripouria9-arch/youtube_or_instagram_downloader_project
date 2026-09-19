from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class ThumbnailWorker(QObject):
    """Fetch thumbnail bytes off the GUI thread."""

    finished = Signal(bytes)
    failed = Signal(str)

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def run(self) -> None:
        import urllib.request

        try:
            with urllib.request.urlopen(self.url, timeout=10) as response:
                data = response.read()
            self.finished.emit(data)
        except Exception as exc:  # pragma: no cover - network
            self.failed.emit(str(exc))
