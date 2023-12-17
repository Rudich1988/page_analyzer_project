SHOW_ALL_WEBSITES = ("SELECT urls.id, urls.name, url_checks.status_code, "
                     "MAX(url_checks.created_at) FROM urls "
                     "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                     "GROUP BY urls.id, url_checks.status_code "
                     "ORDER BY urls.id DESC;")


def get_url_data_request_with_id(id):
    return (f"SELECT urls.id, urls.name, urls.created_at, "
            f"url_checks.id, url_checks.status_code, "
            f"url_checks.h1, url_checks.title, url_checks.description, "
            f"url_checks.created_at FROM urls "
            f"LEFT JOIN url_checks ON urls.id = url_checks.url_id "
            f"WHERE urls.id = {id} ORDER BY url_checks.id DESC;")


def get_url_data_request_with_url(website_url):
    return (f"SELECT urls.id, urls.name, urls.created_at, "
            f"url_checks.id, url_checks.status_code, "
            f"url_checks.h1, url_checks.title, "
            f"url_checks.description, "
            f"url_checks.created_at "
            f"FROM urls LEFT JOIN url_checks "
            f"ON urls.id = url_checks.url_id WHERE "
            f"urls.name = '{website_url}' "
            f"ORDER BY url_checks.id DESC;")


def get_all_urls_with_id(id):
    return f"SELECT * FROM urls WHERE id = {id}"
