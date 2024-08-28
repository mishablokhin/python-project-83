from validators import url, ValidationError
from urllib.parse import urlparse, urlunparse


def is_valid_url(url_to_validate):
    if len(url_to_validate) > 255:
        return False
    try:
        return url(url_to_validate) is True
    except ValidationError:
        return False


def normalize_url(url_to_normalize):
    parsed_url = urlparse(url_to_normalize)
    normalized_url = urlunparse((parsed_url.scheme,
                                 parsed_url.netloc, '', '', '', ''))
    return normalized_url
