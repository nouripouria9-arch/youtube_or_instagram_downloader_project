from app.utils.url_utils import validate_instagram_url, validate_youtube_url


def test_valid_watch_url():
    assert validate_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ') is True


def test_valid_short_url():
    assert validate_youtube_url('https://youtu.be/dQw4w9WgXcQ') is True


def test_invalid_url():
    assert validate_youtube_url('not a url') is False


def test_valid_instagram_reel_url():
    assert validate_instagram_url('https://www.instagram.com/reel/ABC123/') is True


def test_invalid_instagram_profile_url():
    assert validate_instagram_url('https://www.instagram.com/example/') is False
