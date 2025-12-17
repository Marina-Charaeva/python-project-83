
from urllib.parse import urlparse

import validators


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url):
    if len(url) > 255:
        return "URL превышает 255 символов"
    
    if not validators.url(url):
        return "Некорректный URL"
    
    return None