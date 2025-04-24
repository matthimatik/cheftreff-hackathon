def get_origin(url: str) -> str:
    """
    Returns the origin of a URL.
    """
    if url.startswith("https://") or url.startswith("http://"):
        return url.split("/")[2]
    else:
        raise ValueError(f"Invalid URL: {url}")
