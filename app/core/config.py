from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.core.constants import DEFAULT_DOWNLOAD_TYPE, DEFAULT_QUALITY, DEFAULT_THEME, SETTINGS_FILENAME
from app.core.paths import CONFIG_DIR, default_download_dir


@dataclass
class AppSettings:
    theme: str = DEFAULT_THEME
    download_dir: Path = field(default_factory=default_download_dir)
    preferred_quality: str = DEFAULT_QUALITY
    download_type: str = DEFAULT_DOWNLOAD_TYPE
    ffmpeg_path: str = ""
    filename_pattern: str = "{title}"
    max_concurrent_downloads: int = 1
    dark_mode: bool = True
    notifications: bool = True

    @classmethod
    def load(cls, path: Path | None = None) -> "AppSettings":
        config_path = path or CONFIG_DIR / SETTINGS_FILENAME
        if not config_path.exists():
            return cls()
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return cls()

        return cls(
            theme=data.get("theme", DEFAULT_THEME),
            download_dir=Path(data.get("download_dir", str(default_download_dir()))),
            preferred_quality=data.get("preferred_quality", DEFAULT_QUALITY),
            download_type=data.get("download_type", DEFAULT_DOWNLOAD_TYPE),
            ffmpeg_path=data.get("ffmpeg_path", ""),
            filename_pattern=data.get("filename_pattern", "{title}"),
            max_concurrent_downloads=max(1, int(data.get("max_concurrent_downloads", 1))),
            dark_mode=bool(data.get("dark_mode", True)),
            notifications=bool(data.get("notifications", True)),
        )

    def save(self, path: Path | None = None) -> Path:
        config_path = path or CONFIG_DIR / SETTINGS_FILENAME
        config_path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "theme": self.theme,
            "download_dir": str(self.download_dir),
            "preferred_quality": self.preferred_quality,
            "download_type": self.download_type,
            "ffmpeg_path": self.ffmpeg_path,
            "filename_pattern": self.filename_pattern,
            "max_concurrent_downloads": self.max_concurrent_downloads,
            "dark_mode": self.dark_mode,
            "notifications": self.notifications,
        }
        config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return config_path
