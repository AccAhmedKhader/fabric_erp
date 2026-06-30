from django.core.cache import cache
import hashlib
import json
from functools import wraps
def cache_key(prefix, *args, **kwargs):
 key_parts = [prefix]
 if args: key_parts.extend([str(arg) for arg in args])
 if kwargs: key_parts.append(json.dumps(kwargs, sort_keys=True))
 key = '_'.join(key_parts)
 return hashlib.md5(key.encode()).hexdigest()
def cached(timeout=3600):
 def decorator(func):
 @wraps(func)
 def wrapper(*args, **kwargs):
 key = cache_key(func.__name__, *args, **kwargs)
 result = cache.get(key)
 if result is None:
 result = func(*args, **kwargs)
 cache.set(key, result, timeout)
 return result
 return wrapper
 return decorator
def invalidate_cache(prefix):
 def decorator(func):
 @wraps(func)
 def wrapper(*args, **kwargs):
 result = func(*args, **kwargs)
 key = cache_key(prefix)
 cache.delete(key)
 return result
 return wrapper
 return decorator