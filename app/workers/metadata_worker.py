from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from app.core.exceptions import MetadataFetchError
from app.models.video_info import VideoInfo
from app.services.youtube_service import InstagramMetadataService, YouTubeMetadataService


class MetadataWorker(QObject):
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, url: str, platform: str = "youtube") -> None:
        super().__init__()
        self.url = url
        self.platform = platform

    def run(self) -> None:
        try:
            service = InstagramMetadataService if self.platform == "instagram" else YouTubeMetadataService
            data = service.fetch_metadata(self.url)
            self.finished.emit(data)
        except MetadataFetchError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # pragma: no cover - defensive path
            self.failed.emit(str(exc))
