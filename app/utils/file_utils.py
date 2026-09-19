from __future__ import annotations

import re
from pathlib import Path

INVALID_FILENAME_CHARS = '<>:"/\\|?*\0'
# Windows reserved device names (case-insensitive, without extension)
_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
# Conservative limit: 255 per component; whole path may be longer but we cap filename
_MAX_FILENAME_LEN = 200


def safe_filename(name: str, extension: str | None = None) -> str:
    text = (name or "download").strip()
    cleaned = ''.join('_' if ch in INVALID_FILENAME_CHARS else ch for ch in text)
    cleaned = re.sub(r'\s+\.(?=\w)', '.', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = cleaned.strip('.')
    if not cleaned:
        cleaned = 'download'

    # Handle extension first so reserved-name check applies to stem
    ext = ""
    if extension:
        ext = extension if extension.startswith('.') else f'.{extension}'
        if not cleaned.lower().endswith(ext.lower()):
            cleaned = f"{cleaned}{ext}".replace(f" {ext}", ext)

    # Split stem/ext for Windows reserved-name guard
    # ext already includes dot
    stem = cleaned[:-len(ext)] if ext and cleaned.lower().endswith(ext.lower()) else cleaned
    if stem.upper() in _RESERVED_NAMES:
        stem = f"_{stem}"
        cleaned = f"{stem}{ext}" if ext else stem

    # Truncate to avoid MAX_PATH / ENAMETOOLONG.
    # Keep extension intact: truncate stem only.
    if len(cleaned) > _MAX_FILENAME_LEN:
        if ext:
            stem = cleaned[: -len(ext)]
            stem = stem[: max(1, _MAX_FILENAME_LEN - len(ext))]
            cleaned = stem.rstrip(" .") + ext
        else:
            cleaned = cleaned[:_MAX_FILENAME_LEN].rstrip(" .")
        if not cleaned or cleaned == ext:
            cleaned = f"download{ext}" if ext else "download"

    return cleaned


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
