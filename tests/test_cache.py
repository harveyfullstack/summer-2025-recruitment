import pytest
import time
from app.core.cache import SimpleCache


class TestSimpleCache:
    def test_basic_cache_operations(self):
        cache = SimpleCache()

        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

        cache.delete("test_key")
        assert cache.get("test_key") is None

    def test_cache_expiration(self):
        cache = SimpleCache()

        cache.set("expire_key", "expire_value", ttl=1)
        assert cache.get("expire_key") == "expire_value"

        time.sleep(1.1)
        assert cache.get("expire_key") is None

    def test_cache_clear(self):
        cache = SimpleCache()

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_document_caching(self):
        cache = SimpleCache()

        file_content = b"test document content"
        result = {"risk_score": 0.5, "confidence": 0.8}

        key = cache.cache_document_result(file_content, result)
        assert key is not None

        cached_result = cache.get_document_result(file_content)
        assert cached_result == result

    def test_cache_key_generation(self):
        cache = SimpleCache()

        content1 = b"same content"
        content2 = b"same content"
        content3 = b"different content"

        key1 = cache._generate_key("test", content1.decode())
        key2 = cache._generate_key("test", content2.decode())
        key3 = cache._generate_key("test", content3.decode())

        assert key1 == key2
        assert key1 != key3
