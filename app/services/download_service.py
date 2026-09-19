from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from yt_dlp import YoutubeDL

from app.core.exceptions import DownloadCancelledError


@dataclass
class DownloadRequest:
    url: str
    output_dir: str | Path | None = None
    download_type: str = "video"
    quality: str = "best"
    format_id: str | None = None
    filename: str | None = None


class DownloadService:
    """Actual download logic implemented via yt-dlp."""

    def __init__(self) -> None:
        self._cancel_requested = False
        self._cancel_lock = threading.Lock()

    def cancel(self) -> None:
        with self._cancel_lock:
            self._cancel_requested = True

    def reset_cancel(self) -> None:
        with self._cancel_lock:
            self._cancel_requested = False

    def _is_cancelled(self) -> bool:
        with self._cancel_lock:
            return self._cancel_requested

    def run_download(self, request: DownloadRequest, progress_callback: Callable[[dict[str, Any]], None]) -> Path:
        # Reset only if not already cancelled from outside (avoids race where
        # UI called cancel() right before run_download started).
        with self._cancel_lock:
            if not self._cancel_requested:
                self._cancel_requested = False  # explicit no-op keep flag
            else:
                # cancel() was called before run started — honour it immediately
                raise DownloadCancelledError("Download cancelled by user.")

        output_dir = Path(request.output_dir) if request.output_dir else Path.home() / "Downloads"
        output_dir.mkdir(parents=True, exist_ok=True)

        # If caller supplied an explicit filename, honour it (sanitised already
        # via safe_filename in the UI layer); otherwise use yt-dlp title template.
        if request.filename:
            output_template = str(output_dir / request.filename)
            # Ensure placeholder still allows yt-dlp to pick ext when we did not fix it
            if not Path(output_template).suffix:
                output_template = output_template + ".%(ext)s"
        else:
            output_template = str(output_dir / "%(title)s.%(ext)s")

        downloaded_files: list[str] = []

        def progress_hook(event: dict[str, Any]) -> None:
            if self._is_cancelled():
                raise DownloadCancelledError("Download cancelled by user.")
            if event.get("status") == "downloading":
                percent = event.get("_percent_str", "0%")
                speed = event.get("speed") or 0
                eta = event.get("eta")
                downloaded_bytes = event.get("downloaded_bytes") or 0
                total_bytes = event.get("total_bytes") or event.get("total_bytes_estimate") or event.get("total") or 0
                try:
                    pct = float(percent.strip().strip("%")) / 100 if isinstance(percent, str) and "%" in percent else 0.0
                except (ValueError, AttributeError):
                    pct = 0.0
                progress_callback({
                    "status": "downloading",
                    "percent": pct,
                    "speed": speed,
                    "eta": eta,
                    "downloaded_bytes": downloaded_bytes,
                    "total_bytes": total_bytes,
                    "filename": event.get("filename") or request.filename,
                })
            elif event.get("status") == "finished":
                fname = event.get("filename")
                if fname:
                    downloaded_files.append(fname)
                progress_callback({"status": "finished", "filename": fname or request.filename})

        options: dict[str, Any] = {
            "outtmpl": output_template,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [progress_hook],
            "format": request.format_id or request.quality,
        }
        if request.download_type == "audio":
            options["format"] = "bestaudio/best"
            options["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"}]

        try:
            with YoutubeDL(options) as ydl:
                result = ydl.extract_info(request.url, download=True)
        except DownloadCancelledError:
            raise
        except Exception as exc:  # pragma: no cover - network-dependent path
            raise RuntimeError(str(exc)) from exc

        # Prefer the actual filename reported by yt-dlp; fall back to result fields only if needed.
        if downloaded_files:
            return Path(downloaded_files[-1])
        if result and isinstance(result, dict):
            # yt-dlp may expose requested_downloads with filepath
            req_dl = result.get("requested_downloads")
            if isinstance(req_dl, list) and req_dl:
                fp = req_dl[0].get("filepath") or req_dl[0].get("_filename")
                if fp:
                    return Path(fp)
            fp2 = result.get("_filename") or result.get("filepath")
            if fp2:
                return Path(fp2)
        return output_dir
