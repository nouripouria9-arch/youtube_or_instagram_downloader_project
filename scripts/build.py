from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    spec = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name",
        "ProfessionalYouTubeDownloader",
        "--icon",
        str(PROJECT_ROOT / "resources" / "icons" / "app_icon.ico"),
        "app/main.py",
    ]
    subprocess.run(spec, cwd=PROJECT_ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
