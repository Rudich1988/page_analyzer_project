import os

import psycopg2
import requests
from dotenv import load_dotenv
from page_analyzer.find_tags import find_tags
from psycopg2.extras import NamedTupleCursor

SHOW_ALL_WEBSITES = ("SELECT urls.id, urls.name, url_checks.status_code, "
                     "MAX(url_checks.created_at) FROM urls "
                     "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                     "GROUP BY urls.id, url_checks.status_code "
                     "ORDER BY urls.id DESC;")


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_checks(id):
    return (f"SELECT * FROM url_checks "
            f"WHERE url_id = {id} ORDER BY id DESC;")


def get_website(id):
    return (f"SELECT * FROM urls WHERE id = {id};")


def get_url_data_with_id(id):
    return f"SELECT * FROM urls WHERE id = {id}"


def get_url_data_with_website_url(website_url):
    return (f"SELECT * FROM urls WHERE name='{website_url}'")


def connect_database():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def insert_url(website_url):
    conn = connect_database()
    try:
        conn.cursor().execute("INSERT INTO urls (name) "
                              "VALUES (%s)", (website_url,))
        conn.commit()
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(get_url_data_with_website_url(website_url))
            result = cur.fetchone()
        conn.close()
        return {'id': result.id, 'status': 'success'}
    except Exception:
        conn = connect_database()
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(get_url_data_with_website_url(website_url))
            result = cur.fetchone()
        conn.close()
        return {'id': result.id, 'status': 'not success'}


def get_all_urls():
    conn = connect_database()
    with conn.cursor() as cur:
        cur.execute(SHOW_ALL_WEBSITES)
        result = cur.fetchall()
    conn.close()
    return result


def get_url_data_view(id):
    conn = connect_database()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(get_website(id))
        website_data = cur.fetchone()
        cur.execute(get_checks(id))
        checks_website_data = cur.fetchall()
    conn.close()
    return {'website_data': website_data,
            'checks_website_data': checks_website_data}


def check_url_view(id):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(get_url_data_with_id(id))
    result = cur.fetchone()
    url = result.name
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
