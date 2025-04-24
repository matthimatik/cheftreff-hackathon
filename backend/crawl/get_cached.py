from settings import CRAWL_CACHE_DIR
import json
import requests


def get_cached(url: str) -> str:
    """
    Retrieves data from a HTTP Endpoint.
    If the file has been requested before, it will be loaded from the cache.

    WARNING: This function is not thread-safe.
    """
    cache_path = CRAWL_CACHE_DIR / "cache.json"
    if cache_path.exists():
        with open(cache_path, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    cached_data_file = cache.get(url)
    if cached_data_file is not None:
        return (CRAWL_CACHE_DIR / cached_data_file).read_text(encoding="utf-8")

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    data = response.text
    cache_id = len(cache)
    target_file_name = f"{cache_id}.txt"
    cache[url] = target_file_name

    with open(CRAWL_CACHE_DIR / target_file_name, "w", encoding="utf-8") as f:
        f.write(data)

    with open(cache_path, "w") as f:
        json.dump(cache, f)

    return data
