# YouTube / Instagram Downloader

A modular Python desktop downloader project built with **PySide6** and **yt-dlp**, supporting accessible YouTube and Instagram video URLs through a graphical Windows-oriented interface.

> **Project note:** The source code from the provided project archive is kept unchanged. This repository adds project documentation only and stores the original project archive for distribution.

## Overview

This project is organized into separate application layers for the user interface, download/metadata services, workers, models, utilities, configuration, logging, and tests.

At launch, the application lets the user choose between:

- **YouTube Downloader**
- **Instagram Downloader**

The selected downloader then validates the URL, retrieves available metadata, displays thumbnail information when available, and runs the download workflow in background Qt threads.

## Main capabilities

- YouTube and Instagram URL validation
- Video metadata retrieval through `yt-dlp`
- Thumbnail retrieval
- Download directory selection
- Format and quality inputs
- Download progress reporting
- Download cancellation support
- Persistent application settings
- Logging and exception handling
- PySide6 desktop interface with theme support
- Automated tests for configuration, URL validation, file utilities, and download-service behavior

## Technology stack

- **Python 3.11+**
- **PySide6** — desktop graphical user interface
- **yt-dlp** — media metadata and download backend
- **Pillow** — image/icon generation utilities
- **pytest** — automated testing
- **FFmpeg** — required for workflows that need media merging or audio post-processing

## Project structure

```text
youtube_or_instagram_downloader_professional/
├── app/
│   ├── core/          # Configuration, constants, exceptions, logging, paths
│   ├── models/        # Data models
│   ├── services/      # Metadata, download, and FFmpeg services
│   ├── ui/            # PySide6 main window and styles
│   ├── utils/         # URL and file utilities
│   ├── workers/       # Background Qt workers
│   └── main.py        # Application entry point
├── resources/
│   └── icons/         # Application icon resources
├── scripts/
│   ├── build.py       # PyInstaller build helper
│   └── generate_icon.py
├── tests/
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

Create a virtual environment and install the declared dependencies:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux / macOS

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run from source

```bash
python app/main.py
```

## FFmpeg

Install FFmpeg when using workflows that require media merging or audio post-processing. Make sure `ffmpeg` is available on the system `PATH`, or configure its location through the application's settings infrastructure.

## Run tests

```bash
pytest -q
```

## Build

The project includes a PyInstaller helper:

```bash
python scripts/build.py
```

The build helper expects the application icon to exist at:

```text
resources/icons/app_icon.ico
```

The included `scripts/generate_icon.py` can generate the icon assets.

## Project archive

The original project package is stored in this repository as:

```text
youtube_or_instagram_downloader_professional.zip
```

The archive contains the supplied project files without changes to the Python source code.

## Usage and rights

This is an independent third-party project and is not affiliated with YouTube, Instagram, or Meta.

Use the application only with content you are authorized to download and in accordance with the relevant platform terms, copyright rules, and applicable local laws.

## Project status

This repository represents a project snapshot and can be updated as development continues.

---
Developed as a software-engineering / computer-vision student project and organized for continued iteration.
