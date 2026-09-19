from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from app.services.download_service import DownloadRequest, DownloadService


class DownloadWorker(QObject):
    progress = Signal(dict)
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, request: DownloadRequest) -> None:
        super().__init__()
        self.request = request
        self.service = DownloadService()

    def run(self) -> None:
        try:
            output = self.service.run_download(self.request, lambda payload: self.progress.emit(payload))
            self.finished.emit(str(output))
        except Exception as exc:  # pragma: no cover - runtime path
            self.failed.emit(str(exc))

    def cancel(self) -> None:
        self.service.cancel()
