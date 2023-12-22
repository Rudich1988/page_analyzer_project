import os

import psycopg2
import requests
import validators
from dotenv import load_dotenv
from page_analyzer.correct_url import normalize_url
from page_analyzer.find_tags import find_tags
from page_analyzer.psql_requests import (
    SHOW_ALL_WEBSITES,
    get_all_urls_with_id,
    get_url_data_request_with_id,
    get_url_data_request_with_url,
)


LINE_LENGTH = 255

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def is_url_valid(website_url):
    if validators.url(website_url) and len(website_url) <= LINE_LENGTH:
        return True


def connect_database():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def show_urls_view():
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(SHOW_ALL_WEBSITES)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_url_data_view(id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(get_url_data_request_with_id(id))
    checks_website_data = cur.fetchall()
    cur.close()
    conn.close()
    return checks_website_data


def add_website_view(request):
    website_data = request.form.to_dict()
    website_url = normalize_url(website_data['url'])
    if not is_url_valid(website_url):
        return {'website_data': website_data, 'status': 'error'}
    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO urls (name) "
                    "VALUES (%s)", (website_url,))
        conn.commit()
        cur.execute(get_url_data_request_with_url(website_url))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {'id': result[0], 'status': 'success'}
    except Exception:
        conn = connect_database()
        cur = conn.cursor()
        cur.execute(get_url_data_request_with_url(website_url))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {'id': result[0], 'status': 'not success'}


def check_url_view(id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute(get_all_urls_with_id(id))
    result = cur.fetchone()
    url = result[1]
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code != 200:
            return 'error'
        tags = find_tags(response)
        title = tags['title']
        h1 = tags['h1']
        description = tags['description']
        cur.execute("INSERT INTO url_checks (url_id, status_code, h1, "
                    "title, description) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id, status_code, h1, title, description))
        conn.commit()
        cur.close()
        conn.close()
        return 'success'
    except Exception:
        return 'error'
