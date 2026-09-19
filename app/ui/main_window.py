from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.core.config import AppSettings
from app.core.logger import build_logger
from app.core.paths import default_download_dir
from app.core.constants import INSTAGRAM_PLATFORM
from app.models.video_info import VideoInfo
from app.services.download_service import DownloadRequest
from app.utils.file_utils import safe_filename
from app.utils.url_utils import validate_instagram_url, validate_youtube_url
from app.workers.download_worker import DownloadWorker
from app.workers.metadata_worker import MetadataWorker
from app.workers.thumbnail_worker import ThumbnailWorker

logger = build_logger("app.ui.main_window")


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings, platform: str = "youtube") -> None:
        super().__init__()
        self.settings = settings
        self.platform = platform
        self.metadata: VideoInfo | None = None
        self.current_thread: QThread | None = None
        self.current_worker: DownloadWorker | None = None
        self._meta_thread: QThread | None = None
        self._meta_worker: MetadataWorker | None = None
        self._thumb_thread: QThread | None = None
        self._thumb_worker: ThumbnailWorker | None = None
        self.platform_name = "Instagram" if platform == INSTAGRAM_PLATFORM else "YouTube"
        self.setWindowTitle(f"Professional {self.platform_name} Downloader")
        self.resize(1000, 720)
        self._build_ui()

    def _build_ui(self) -> None:
        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(24, 18, 24, 18)
        self.layout.setSpacing(18)

        header = QHBoxLayout()
        title = QLabel(f"Professional {self.platform_name} Downloader")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        header.addWidget(title)
        header.addStretch()

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self._open_settings)
        header.addWidget(self.settings_button)
        self.layout.addLayout(header)

        url_row = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(f"Paste an {self.platform_name} URL here")
        self.url_input.returnPressed.connect(self.analyze_url)
        url_row.addWidget(self.url_input)

        self.paste_button = QPushButton("Paste")
        self.paste_button.clicked.connect(self._paste_url)
        url_row.addWidget(self.paste_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_url)
        url_row.addWidget(self.clear_button)

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_url)
        url_row.addWidget(self.analyze_button)
        self.layout.addLayout(url_row)

        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)

        metadata_panel = QWidget()
        metadata_layout = QVBoxLayout(metadata_panel)
        self.thumbnail_label = QLabel("Thumbnail preview")
        self.thumbnail_label.setMinimumSize(260, 180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setStyleSheet("background: #1f2937; border-radius: 12px; color: #f8fafc;")
        metadata_layout.addWidget(self.thumbnail_label)

        self.meta_title = QLabel("No video selected")
        self.meta_title.setWordWrap(True)
        self.meta_title.setStyleSheet("font-size: 18px; font-weight: 600;")
        metadata_layout.addWidget(self.meta_title)

        self.meta_details = QLabel(f"Enter a valid {self.platform_name} URL to load metadata.")
        self.meta_details.setWordWrap(True)
        metadata_layout.addWidget(self.meta_details)
        self.layout.addWidget(metadata_panel)

        options_layout = QFormLayout()
        self.output_dir_edit = QLineEdit(str(self.settings.download_dir))
        self.output_dir_edit.setReadOnly(True)
        self.output_dir_select = QPushButton("Choose folder")
        self.output_dir_select.clicked.connect(self._choose_output_dir)
        options_layout.addRow("Output directory", self.output_dir_edit)
        options_layout.addRow("", self.output_dir_select)

        self.format_combo = QLineEdit("mp4")
        options_layout.addRow("Format", self.format_combo)

        self.quality_combo = QLineEdit("best")
        options_layout.addRow("Quality", self.quality_combo)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        options_layout.addRow("", self.download_button)
        self.layout.addLayout(options_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Idle")
        self.layout.addWidget(self.progress_label)

    def _open_settings(self) -> None:
        self.status_label.setText("Settings panel is available for future expansion.")

    def _paste_url(self) -> None:
        clipboard = QApplication.clipboard()
        if clipboard:
            self.url_input.setText(clipboard.text())

    def _clear_url(self) -> None:
        self.url_input.clear()
        self.metadata = None
        self.meta_title.setText("No video selected")
        self.meta_details.setText(f"Enter a valid {self.platform_name} URL to load metadata.")
        self.progress_label.setText("Idle")

    def _choose_output_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select download directory", str(self.settings.download_dir))
        if directory:
            self.output_dir_edit.setText(directory)
            self.settings.download_dir = Path(directory)

    # ── helpers: thread cleanup ──────────────────────────────────────────
    def _cleanup_thread(self, thread: QThread) -> None:
        thread.quit()
        thread.wait(3000)
        thread.deleteLater()

    def _is_thread_running(self, thread: QThread | None) -> bool:
        return thread is not None and thread.isRunning()

    # ── metadata flow ────────────────────────────────────────────────────
    def analyze_url(self) -> None:
        url = self.url_input.text().strip()
        validator = validate_instagram_url if self.platform == INSTAGRAM_PLATFORM else validate_youtube_url
        if not validator(url):
            QMessageBox.warning(self, "Invalid URL", f"Please enter a valid {self.platform_name} URL.")
            return

        if self._is_thread_running(self._meta_thread):
            QMessageBox.information(self, "Please wait", "Already fetching metadata. Please wait.")
            return

        self.status_label.setText("Fetching video information...")
        self.analyze_button.setEnabled(False)

        worker = MetadataWorker(url, self.platform)
        thread = QThread(self)
        self._meta_worker = worker
        self._meta_thread = thread
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._handle_metadata_success)
        worker.failed.connect(self._handle_metadata_failure)
        # Always quit + cleanup on either outcome
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: setattr(self, "_meta_thread", None))
        thread.finished.connect(lambda: setattr(self, "_meta_worker", None))
        thread.start()

    def _handle_metadata_success(self, video: VideoInfo) -> None:
        self.metadata = video
        self.analyze_button.setEnabled(True)
        self.status_label.setText("Video information loaded.")
        self.meta_title.setText(video.title)
        self.meta_details.setText(
            f"Uploader: {video.uploader} | Duration: {video.duration_text} | Views: {video.view_count or 'N/A'}"
        )
        if video.thumbnail_url:
            self._fetch_thumbnail_async(video.thumbnail_url)

    def _handle_metadata_failure(self, error: str) -> None:
        self.analyze_button.setEnabled(True)
        self.status_label.setText(error)
        QMessageBox.critical(self, "Metadata error", error)

    # ── thumbnail (off GUI thread) ───────────────────────────────────────
    def _fetch_thumbnail_async(self, url: str) -> None:
        if self._is_thread_running(self._thumb_thread):
            # let previous thumb fetch finish; start new one after
            try:
                self._thumb_thread.quit()
                self._thumb_thread.wait(2000)
            except Exception:
                pass
        worker = ThumbnailWorker(url)
        thread = QThread(self)
        self._thumb_worker = worker
        self._thumb_thread = thread
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._on_thumbnail_data)
        worker.failed.connect(lambda _e: None)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: setattr(self, "_thumb_thread", None))
        thread.finished.connect(lambda: setattr(self, "_thumb_worker", None))
        thread.start()

    def _on_thumbnail_data(self, data: bytes) -> None:
        if not data:
            return
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        if not pixmap.isNull():
            self.thumbnail_label.setPixmap(pixmap.scaled(260, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # ── download flow ────────────────────────────────────────────────────
    def start_download(self) -> None:
        if not self.metadata:
            QMessageBox.warning(self, "No metadata", f"Analyze a valid {self.platform_name} URL before downloading.")
            return

        if self._is_thread_running(self.current_thread):
            QMessageBox.information(self, "Download in progress", "A download is already running. Please wait or cancel it.")
            return

        target_dir = self.output_dir_edit.text().strip() or str(default_download_dir())
        request = DownloadRequest(
            url=self.metadata.webpage_url,
            output_dir=target_dir,
            download_type="video",
            quality=self.quality_combo.text().strip() or "best",
            format_id=self.format_combo.text().strip() or None,
            filename=safe_filename(self.metadata.title, ".mp4"),
        )

        self.status_label.setText("Preparing download...")
        self.progress_bar.setValue(0)
        self.download_button.setEnabled(False)
        worker = DownloadWorker(request)
        thread = QThread(self)
        worker.moveToThread(thread)
        self.current_thread = thread
        self.current_worker = worker
        thread.started.connect(worker.run)
        worker.progress.connect(self._handle_progress)
        worker.finished.connect(self._handle_download_complete)
        worker.failed.connect(self._handle_download_failure)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.failed.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: setattr(self, "current_thread", None))
        thread.finished.connect(lambda: setattr(self, "current_worker", None))
        thread.finished.connect(lambda: self.download_button.setEnabled(True))
        thread.start()

    def _handle_progress(self, payload: dict) -> None:
        percent = payload.get("percent", 0.0)
        try:
            pct = float(percent)
        except (TypeError, ValueError):
            pct = 0.0
        self.progress_bar.setValue(int(max(0.0, min(1.0, pct)) * 100))
        self.progress_label.setText(f"{payload.get('status', 'downloading')} - {payload.get('filename', 'video')}")

    def _handle_download_complete(self, output: str) -> None:
        self.status_label.setText("Download completed")
        self.progress_label.setText(f"Saved to: {output}")
        self.progress_bar.setValue(100)
        self.download_button.setEnabled(True)

    def _handle_download_failure(self, error: str) -> None:
        self.status_label.setText(error)
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Download failed", error)

    def closeEvent(self, event) -> None:  # type: ignore[override]
        for t in (self.current_thread, self._meta_thread, self._thumb_thread):
            if self._is_thread_running(t):
                try:
                    if self.current_worker:
                        self.current_worker.cancel()
                    t.quit()
                    t.wait(3000)
                except Exception:
                    pass
        super().closeEvent(event)
