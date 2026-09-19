from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VideoInfo:
    id: str
    title: str
    uploader: str = "Unknown"
    duration: int = 0
    thumbnail_url: str = ""
    upload_date: str = ""
    view_count: int | None = None
    webpage_url: str = ""
    formats: list[dict[str, Any]] = field(default_factory=list)
    available: bool = True

    @property
    def duration_text(self) -> str:
        minutes, seconds = divmod(self.duration, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"
