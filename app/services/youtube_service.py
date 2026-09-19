from __future__ import annotations

import re
from typing import Any

from yt_dlp import YoutubeDL

from app.core.exceptions import MetadataFetchError
from app.models.video_info import VideoInfo
from app.utils.url_utils import validate_instagram_url, validate_youtube_url


class _MetadataService:
    """Fetch metadata for a YouTube URL using yt-dlp."""

    validator = staticmethod(validate_youtube_url)
    platform_name = "YouTube"

    @classmethod
    def fetch_metadata(cls, url: str) -> VideoInfo:
        if not cls.validator(url):
            raise MetadataFetchError(f"The provided URL is not a valid {cls.platform_name} link.")

        options: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
        }

        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as exc:  # pragma: no cover - network-dependent path
            raise MetadataFetchError(str(exc)) from exc

        if not info:
            raise MetadataFetchError("No metadata could be retrieved for the requested URL.")

        raw_id = info.get("id")
        if raw_id:
            video_id: str | re.Match | None = str(raw_id)
        elif cls.platform_name == "YouTube":
            video_id = re.search(r"(?:v=|/)([A-Za-z0-9_-]{11})", url)
            if isinstance(video_id, re.Match):
                video_id = video_id.group(1)
        else:
            # Instagram: shortcode is path segment, not 11-char YouTube id
            m = re.search(r"/(?:p|reel|reels|tv)/([^/?#&]+)", url)
            video_id = m.group(1) if m else None
        duration = int(info.get("duration") or 0)
        uploader = info.get("uploader") or "Unknown"
        title = info.get("title") or "Unknown title"
        thumbnail_url = (info.get("thumbnail") or "")
        view_count = info.get("view_count")
        upload_date = info.get("upload_date") or ""
        webpage_url = info.get("webpage_url") or url

        formats = info.get("formats") or []
        return VideoInfo(
            id=str(video_id or "unknown"),
            title=title,
            uploader=uploader,
            duration=duration,
            thumbnail_url=thumbnail_url,
            upload_date=upload_date,
            view_count=int(view_count) if view_count is not None else None,
            webpage_url=webpage_url,
            formats=formats,
            available=True,
        )


class YouTubeMetadataService(_MetadataService):
    """Fetch metadata for a YouTube URL using yt-dlp."""


class InstagramMetadataService(_MetadataService):
    """Fetch metadata for an accessible Instagram video using yt-dlp."""

    validator = staticmethod(validate_instagram_url)
    platform_name = "Instagram"
