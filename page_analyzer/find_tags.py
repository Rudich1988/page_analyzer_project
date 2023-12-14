from bs4 import BeautifulSoup as bs
import requests


def find_tags(response):
    soup = bs(response.text, 'html.parser')
    tags = [soup.title, soup.h1, soup.description]
    normalize_tags = []
    for tag in tags:
        if tag is None:
            normalize_tags.append('')
        else:
            normalize_tags.append(tag.text)
    return {'title': normalize_tags[0], 'h1': normalize_tags[1],
            'description': normalize_tags[2]}
