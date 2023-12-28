from urllib.parse import urlparse

import validators

LINE_LENGTH = 255


def is_url_valid(website_url):
    return validators.url(website_url) and len(website_url) <= LINE_LENGTH


def normalize_url(website_name):
    url_parser = urlparse(website_name)
    normal_url = url_parser.scheme.lower() + '://' + url_parser.netloc.lower()
    return normal_url
