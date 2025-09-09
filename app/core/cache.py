import time
from typing import Any, Optional, Dict
import hashlib


class SimpleCache:
    def __init__(self, default_ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self._stats = {"hits": 0, "misses": 0, "sets": 0}

    def _generate_key(self, prefix: str, data: str) -> str:
        hash_obj = hashlib.md5(data.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires"]:
                self._stats["hits"] += 1
                return entry["value"]
            else:
                del self._cache[key]
        self._stats["misses"] += 1
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires = time.time() + (ttl or self.default_ttl)
        self._cache[key] = {"value": value, "expires": expires}
        self._stats["sets"] += 1

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
        self._stats = {"hits": 0, "misses": 0, "sets": 0}

    def get_stats(self) -> Dict[str, Any]:
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "sets": self._stats["sets"],
            "hit_rate": round(hit_rate, 3),
            "cache_size": len(self._cache),
        }

    def cache_document_result(
        self, file_content: bytes, result: Any, ttl: int = 1800
    ) -> str:
        content_hash = hashlib.md5(file_content).hexdigest()
        key = f"doc:{content_hash}"
        self.set(key, result, ttl)
        return key

    def get_document_result(self, file_content: bytes) -> Optional[Any]:
        content_hash = hashlib.md5(file_content).hexdigest()
        key = f"doc:{content_hash}"
        return self.get(key)


cache = SimpleCache()
