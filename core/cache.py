"""
Cache management for API responses and data.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Any, Dict
from functools import wraps
from contextlib import contextmanager

from core.config import AppConfig

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching for API responses and scraped data."""
    
    def __init__(self, config: AppConfig, cache_dir: str = ".cache"):
        self.config = config
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache: Dict[str, dict] = {}
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a hash-based cache key."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the file path for a cache entry."""
        return self.cache_dir / f"{self._get_cache_key(key)}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache (memory first, then disk)."""
        cache_key = self._get_cache_key(key)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if self._is_valid(entry):
                return entry.get('data')
            else:
                del self.memory_cache[cache_key]
        
        # Check disk cache
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                if self._is_valid(entry):
                    # Promote to memory cache
                    self.memory_cache[cache_key] = entry
                    return entry.get('data')
                else:
                    cache_path.unlink()  # Delete expired cache
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        return None
    
    def set(self, key: str, data: Any, ttl_hours: Optional[int] = None) -> None:
        """Set a value in cache (both memory and disk)."""
        ttl = ttl_hours or self.config.cache_ttl_hours
        cache_key = self._get_cache_key(key)
        
        entry = {
            'data': data,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ttl_hours': ttl
        }
        
        # Store in memory
        self.memory_cache[cache_key] = entry
        
        # Enforce cache size limit
        if len(self.memory_cache) > self.config.cache_max_size:
            oldest_key = next(iter(self.memory_cache))
            del self.memory_cache[oldest_key]
        
        # Store on disk
        try:
            cache_path = self._get_cache_path(key)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(entry, f)
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def _is_valid(self, entry: dict) -> bool:
        """Check if a cache entry is still valid."""
        try:
            timestamp_str = entry.get('timestamp', '')
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'
            timestamp = datetime.fromisoformat(timestamp_str)
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            ttl_hours = entry.get('ttl_hours', self.config.cache_ttl_hours)
            expiry = timestamp + timedelta(hours=ttl_hours)
            return datetime.now(timezone.utc) < expiry
        except Exception:
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception:
                pass
    
    def invalidate(self, key: str) -> None:
        """Invalidate a specific cache entry."""
        cache_key = self._get_cache_key(key)
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
        
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                cache_path.unlink()
            except Exception:
                pass


def cached(cache_manager: CacheManager, key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            if result is not None:
                cache_manager.set(cache_key, result)
            
            return result
        return wrapper
    return decorator


@contextmanager
def timed_operation(name: str):
    """Context manager for timing operations."""
    start = datetime.now(timezone.utc)
    try:
        yield
    finally:
        elapsed = (datetime.now(timezone.utc) - start).total_seconds()
        logger.debug(f"{name} completed in {elapsed:.2f}s")
