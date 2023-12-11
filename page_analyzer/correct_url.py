from urllib.parse import urlparse


def normalize_url(website_name):
    url_parser = urlparse(website_name)
    normal_url = url_parser.scheme.lower() + '://' + url_parser.netloc.lower()
    return normal_url
