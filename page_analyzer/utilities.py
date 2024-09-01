from validators import url, ValidationError
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup


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


def make_request_to_url(url):
    try:
        site_request = requests.get(url)
        site_request.raise_for_status()
    except requests.exceptions.RequestException as err:
        return err
    else:
        if site_request.status_code == 200:
            return 200


def get_site_html_content(site_url):
    response = requests.get(site_url)
    html_content = response.text
    return html_content


def parse_site(content):
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
