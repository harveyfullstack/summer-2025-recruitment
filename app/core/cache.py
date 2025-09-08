import time
from typing import Any, Optional, Dict
import hashlib


class SimpleCache:
    def __init__(self, default_ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def _generate_key(self, prefix: str, data: str) -> str:
        hash_obj = hashlib.md5(data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires"]:
                return entry["value"]
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires = time.time() + (ttl or self.default_ttl)
        self._cache[key] = {"value": value, "expires": expires}

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()

    def cache_document_result(
        self, file_content: bytes, result: Any, ttl: int = 1800
    ) -> str:
        key = self._generate_key("doc", file_content.decode("utf-8", errors="ignore"))
        self.set(key, result, ttl)
        return key

    def get_document_result(self, file_content: bytes) -> Optional[Any]:
        key = self._generate_key("doc", file_content.decode("utf-8", errors="ignore"))
        return self.get(key)


cache = SimpleCache()
