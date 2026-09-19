from app.services.download_service import DownloadRequest


def test_download_request_defaults():
    request = DownloadRequest(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert request.url.startswith('https://')
    assert request.download_type == 'video'
