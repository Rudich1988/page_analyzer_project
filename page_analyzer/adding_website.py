import validators
from page_analyzer.correct_url import normalize_url
from page_analyzer.db import insert_url

LINE_LENGTH = 255


def is_url_valid(website_url):
    if validators.url(website_url) and len(website_url) <= LINE_LENGTH:
        return True


def add_website_view(request):
    website_data = request.form.to_dict()
    website_url = normalize_url(website_data['url'])
    if not is_url_valid(website_url):
        return {'website_data': website_data, 'status': 'error'}
    return insert_url(website_url)
