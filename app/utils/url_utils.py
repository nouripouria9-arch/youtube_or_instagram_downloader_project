from __future__ import annotations

from urllib.parse import urlparse


YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "music.youtube.com",
    "www.youtu.be",
}
INSTAGRAM_HOSTS = {
    "instagram.com",
    "www.instagram.com",
    "m.instagram.com",
}


def validate_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    cleaned = url.strip()
    if not cleaned:
        return False
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    # Strip userinfo and port, then normalise.
    host = parsed.netloc.lower().split("@")[-1].split(":")[0]
    return host in YOUTUBE_HOSTS


def validate_instagram_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    cleaned = url.strip()
    if not cleaned:
        return False
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    host = parsed.netloc.lower().split(":", 1)[0]
    return host in INSTAGRAM_HOSTS and any(
        parsed.path.lower().startswith(prefix)
        for prefix in ("/p/", "/reel/", "/reels/", "/tv/")
    )


def normalize_url(url: str) -> str:
    return url.strip()
