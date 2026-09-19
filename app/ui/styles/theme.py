from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette


DARK_THEME = {
    "bg": "#0f172a",
    "panel": "#111827",
    "panel_alt": "#1f2937",
    "card": "#111827",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "accent": "#ef4444",
    "accent_soft": "#f87171",
    "success": "#22c55e",
    "warning": "#fbbf24",
    "danger": "#ef4444",
    "border": "#334155",
}

LIGHT_THEME = {
    "bg": "#f3f4f6",
    "panel": "#ffffff",
    "panel_alt": "#e5e7eb",
    "card": "#ffffff",
    "text": "#111827",
    "muted": "#6b7280",
    "accent": "#ef4444",
    "accent_soft": "#fca5a5",
    "success": "#16a34a",
    "warning": "#f59e0b",
    "danger": "#dc2626",
    "border": "#d1d5db",
}


def apply_palette(app, theme_name: str) -> None:
    palette = QPalette()
    colors = DARK_THEME if theme_name == "dark" else LIGHT_THEME
    palette.setColor(QPalette.Window, QColor(colors["bg"]))
    palette.setColor(QPalette.WindowText, QColor(colors["text"]))
    palette.setColor(QPalette.Base, QColor(colors["panel"]))
    palette.setColor(QPalette.AlternateBase, QColor(colors["panel_alt"]))
    palette.setColor(QPalette.ToolTipBase, QColor(colors["panel"]))
    palette.setColor(QPalette.ToolTipText, QColor(colors["text"]))
    palette.setColor(QPalette.Text, QColor(colors["text"]))
    palette.setColor(QPalette.Button, QColor(colors["panel"]))
    palette.setColor(QPalette.ButtonText, QColor(colors["text"]))
    palette.setColor(QPalette.Highlight, QColor(colors["accent"]))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)
    app.setStyleSheet(
        f"QWidget {{ background-color: {colors['bg']}; color: {colors['text']}; }} "
        f"QLineEdit, QComboBox, QTextEdit, QListWidget, QTableWidget {{ background: {colors['panel']}; color: {colors['text']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 6px; }} "
        f"QPushButton {{ background: {colors['panel']}; color: {colors['text']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 8px 14px; }} "
        f"QPushButton:hover {{ background: {colors['panel_alt']}; }} "
        f"QPushButton:pressed {{ background: {colors['accent']}; color: white; }} "
        f"QProgressBar {{ border: 1px solid {colors['border']}; border-radius: 8px; background: {colors['panel_alt']}; }} "
        f"QProgressBar::chunk {{ background: {colors['accent']}; border-radius: 7px; }} "
    )
