from validators import url
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def is_valid_url(url_to_validate):
    if len(url_to_validate) > 255:
        return False
    return url(url_to_validate)


def normalize_url(url_to_normalize):
    parsed_url = urlparse(url_to_normalize)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return normalized_url


def get_seo_information_from_page(content):
    site_data = {
        'h1': '',
        'title': '',
        'description': ''
    }
    soup = BeautifulSoup(content, 'html.parser')
    if soup.h1:
        site_data['h1'] = soup.h1.text
    if soup.title:
        site_data['title'] = soup.title.text
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        site_data['description'] = meta_tag.get('content')
    return site_data
