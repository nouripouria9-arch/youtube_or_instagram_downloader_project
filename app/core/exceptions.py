from __future__ import annotations


class DownloaderError(Exception):
    """Base application exception."""


class InvalidUrlError(DownloaderError):
    """Raised when a URL is invalid."""


class MetadataFetchError(DownloaderError):
    """Raised when metadata retrieval fails."""


class FfmpegNotFoundError(DownloaderError):
    """Raised when FFmpeg could not be found."""


class DownloadCancelledError(DownloaderError):
    """Raised when a download is cancelled."""
