import psycopg2
from psycopg2.extras import NamedTupleCursor

from page_analyzer import app


def connect_database():
    conn = psycopg2.connect(app.app.config['DATABASE_URL'])
    return conn


def insert_url(website_url):
    conn = connect_database()
    try:
        cur = conn.cursor()
        with conn.cursor() as cur:#cur.execute("INSERT INTO urls (name) "
            cur.execute("INSERT INTO urls (name) "
                        "VALUES (%s) RETURNING id;", (website_url,))                     #"VALUES (%s) RETURNING id;", (website_url,))
        id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return {'id': id}
    #except Exception:
     #   return BaseException#None
    except Exception:
        conn.close()
        raise ValueError()
    #conn = connect_database()
    #with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
     #   cur.execute(f"SELECT * FROM urls WHERE name='{website_url}'")
      #  result = cur.fetchone()
    


def get_all_urls():
    conn = connect_database()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT urls.id, urls.name, url_checks.status_code, "
                    "MAX(url_checks.created_at) FROM urls "
                    "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                    "GROUP BY urls.id, url_checks.status_code "
                    "ORDER BY urls.id DESC;")
        result = cur.fetchall()
    conn.close()
    return result


def get_url_checks(id):
    conn = connect_database()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(f"SELECT * FROM urls WHERE id = {id};")
        website_data = cur.fetchone()
        cur.execute(f"SELECT * FROM url_checks "
                    f"WHERE url_id = {id} ORDER BY id DESC;")
        checks_website_data = cur.fetchall()
    conn.close()
    return website_data, checks_website_data


def get_url_name(id):
    conn = connect_database()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(f"SELECT * FROM urls WHERE id = {id}")
        result = cur.fetchone()
    conn.close()
    return result.name


def get_url_id(website_url):
    conn = connect_database()
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(f"SELECT id FROM urls WHERE name = '{website_url}'")
        result = cur.fetchone()
    conn.close()
    return result.id


def insert_url_checks(id, status_code, title, h1, description):
    conn = connect_database()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    try:
        cur.execute("INSERT INTO url_checks (url_id, status_code, h1, "
                    "title, description) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id, status_code, h1, title, description))
        conn.commit()
        cur.close()
        conn.close()
        return id
    except Exception:
        raise ValueError()
