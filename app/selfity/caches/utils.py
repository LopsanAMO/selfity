import zlib
import json
from django.core.cache import caches


def cache_object(obj, cache_name, cache_key):
    compressed_all = zlib.compress(
        json.dumps(obj, separators=(',', ':')).encode('utf-8'), 9)
    caches[cache_name].set(cache_key, compressed_all, timeout=None)


def cache_instance(instance, serializer, cache_name):
    serialized_object = serializer(instance=instance).data
    cache_object(serialized_object, cache_name, instance.phone_number)
    return serialized_object


def get_cached_object(lookup, cache_name='users'):
    cached_object = caches[cache_name].get(lookup)
    if cached_object:
        return json.loads(zlib.decompress(cached_object), encoding='utf-8')
    return cached_object


def delete_cached_object(lookup, cache_name='users'):
    caches[cache_name].delete(lookup)