# YouTube / Instagram Downloader

A modular Python desktop application for downloading accessible YouTube and Instagram video URLs through a graphical **PySide6** interface with **yt-dlp** as the media backend.

> **Source-code note:** The supplied project source has been added to this repository without intentional changes to the application's code logic. Repository work is limited to organizing the supplied source and adding documentation.

## Overview

At startup, the application lets the user choose between:

- **YouTube Downloader**
- **Instagram Downloader**

The selected workflow validates the URL, retrieves available metadata, loads a thumbnail when available, and performs the download in a background Qt worker.

## Main capabilities

- YouTube and Instagram URL validation
- Metadata retrieval through `yt-dlp`
- Thumbnail retrieval
- Download directory selection
- Format and quality inputs
- Download progress reporting
- Download cancellation support
- Persistent application settings
- Logging and exception handling
- PySide6 desktop interface
- Automated tests for configuration, URL validation, file utilities, and download-service behavior

## Technology stack

- **Python 3.11+**
- **PySide6** — desktop graphical user interface
- **yt-dlp** — media metadata and download backend
- **Pillow** — image/icon generation utilities
- **pytest** — automated testing
- **FFmpeg** — used by workflows that require media merging or audio post-processing

## Project structure

```text
youtube_or_instagram_downloader_project/
├── app/
│   ├── core/          # Configuration, constants, exceptions, logging, paths
│   ├── models/        # Application data models
│   ├── services/      # Metadata, download, and FFmpeg services
│   ├── ui/            # PySide6 main window and theme
│   ├── utils/         # URL and file utilities
│   ├── workers/       # Background Qt workers
│   └── main.py        # Application entry point
├── scripts/
│   ├── build.py       # PyInstaller build helper
│   └── generate_icon.py
├── tests/
├── .gitignore
├── pyproject.toml
├── pyrightconfig.json
├── requirements.txt
├── PROJECT_DESCRIPTION.md
└── README.md
```

## Installation

Create a virtual environment:

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

Install FFmpeg when a workflow requires media merging or audio post-processing. The executable should be available on the system `PATH`, or its location can be supplied through the application's configuration infrastructure.

## Run tests

```bash
pytest -q
```

## Build

The project includes a PyInstaller helper:

```bash
python scripts/build.py
```

The build helper expects:

```text
resources/icons/app_icon.ico
```

The included `scripts/generate_icon.py` can generate the icon assets used by the build configuration.

## Development notes

The repository is intended as an evolving project snapshot. Additional features, tests, UI improvements, and platform-specific adjustments can be added through future commits without changing the original source unnecessarily.

## Usage and rights

This is an independent third-party project and is not affiliated with YouTube, Instagram, or Meta.

Use the application only with content you are authorized to download and in accordance with the relevant platform terms, copyright rules, and applicable local laws.

---
Written by Pouria Nouri
Student of Computer Engineering (specializing in AI, image processing, and computer vision), front-end designer, and application developer.
