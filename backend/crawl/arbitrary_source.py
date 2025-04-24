from cite_manager import CiteManager
from crawl.get_cached import get_cached
from utils import get_origin


def url_encode_model(url: str, cite_manager: CiteManager) -> str:
    """
    Retrieves data from a HTTP Endpoint.
    If the file has been requested before, it will be loaded from the cache.

    WARNING: This function is not thread-safe.
    """
    text = get_cached(url)

    cite_id = cite_manager.register_cite(url, get_origin(url))
    return f"<ARTICLE><ID>{cite_id}</ID><BODY>{text}</BODY>"
