from app.core.config import AppSettings


def test_default_settings():
    settings = AppSettings()
    assert settings.download_dir.name == 'Downloads'
    assert settings.theme in {'dark', 'light'}
