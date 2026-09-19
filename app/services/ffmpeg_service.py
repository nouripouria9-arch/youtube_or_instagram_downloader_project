from __future__ import annotations

import os
import shutil
from pathlib import Path

from app.core.exceptions import FfmpegNotFoundError


class FFmpegService:
    """Detect and validate FFmpeg installation."""

    @staticmethod
    def find_ffmpeg() -> str:
        candidates = ["ffmpeg", "ffmpeg.exe"]
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved:
                return resolved
        return ""

    @classmethod
    def ensure_available(cls, custom_path: str | None = None) -> str:
        path = (custom_path or "").strip().strip('"').strip("'")
        if path:
            p = Path(path)
            if p.is_dir():
                raise FfmpegNotFoundError(
                    f"FFmpeg path is a directory, not an executable: {p}. "
                    "Point it to the ffmpeg binary (e.g. C:\ffmpeg\bin\ffmpeg.exe)."
                )
            if p.is_file():
                if not os.access(p, os.X_OK) and os.name != "nt":
                    raise FfmpegNotFoundError(f"FFmpeg at {p} is not executable.")
                return str(p)
            # Non-existent custom path — fall through to PATH lookup
            # (do not silently accept it)
        resolved = cls.find_ffmpeg()
        if not resolved:
            raise FfmpegNotFoundError(
                "FFmpeg was not found. Install it and add it to PATH or configure the path in settings."
            )
        return resolved
