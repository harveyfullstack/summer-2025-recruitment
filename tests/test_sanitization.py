import pytest
from app.core.sanitizer import InputSanitizer


class TestInputSanitizer:
    def test_sanitize_email_valid(self):
        result = InputSanitizer.sanitize_email("test@example.com")
        assert result == "test@example.com"

    def test_sanitize_email_invalid(self):
        assert InputSanitizer.sanitize_email("invalid-email") is None
        assert InputSanitizer.sanitize_email("") is None
        assert InputSanitizer.sanitize_email("a" * 255 + "@test.com") is None

    def test_sanitize_phone_valid(self):
        result = InputSanitizer.sanitize_phone("(555) 123-4567")
        assert result == "(555) 123-4567"

    def test_sanitize_phone_invalid(self):
        assert InputSanitizer.sanitize_phone("123") is None
        assert InputSanitizer.sanitize_phone("") is None
        assert InputSanitizer.sanitize_phone("a" * 25) is None

    def test_sanitize_text_removes_control_chars(self):
        text_with_control = "Hello\x00\x08World\x1f"
        result = InputSanitizer.sanitize_text(text_with_control)
        assert result == "HelloWorld"

    def test_sanitize_text_length_limit(self):
        long_text = "a" * 6000
        result = InputSanitizer.sanitize_text(long_text, 5000)
        assert len(result) == 5000

    def test_sanitize_ip_valid(self):
        assert InputSanitizer.sanitize_ip("192.168.1.1") == "192.168.1.1"
        assert InputSanitizer.sanitize_ip("::1") == "::1"

    def test_sanitize_ip_invalid(self):
        assert InputSanitizer.sanitize_ip("999.999.999.999") is None
        assert InputSanitizer.sanitize_ip("") is None
        assert InputSanitizer.sanitize_ip("a" * 50) is None
