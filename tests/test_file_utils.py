from app.utils.file_utils import safe_filename


def test_safe_filename_removes_invalid_chars():
    value = safe_filename('video<>:"/\|?* .mp4')
    assert value == 'video_________.mp4'


def test_safe_filename_trims_whitespace():
    assert safe_filename('  sample title  ') == 'sample title'
