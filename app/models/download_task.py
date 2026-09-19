from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class DownloadTask:
    id: str
    url: str
    title: str = "Unknown"
    status: str = "queued"
    output_path: str | None = None
    format_id: str | None = None
    ext: str = "mp4"
    progress: float = 0.0
    speed: str = "0 KB/s"
    eta: str = "--:--"
    downloaded: str = "0 B"
    total: str = "0 B"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def output_path_obj(self) -> Path | None:
        return Path(self.output_path) if self.output_path else None
