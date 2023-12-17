import os
#from datetime import date

#import psycopg2
#import requests
#import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
#from page_analyzer.correct_url import normalize_url
#from page_analyzer.find_tags import find_tags
from page_analyzer.logic_views import show_urls_view, get_url_data_view, add_website_view, check_url_view

app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app.secret_key = "secret_key"


@app.route('/')
def show_form():
    website_name = {'url': ''}
    return render_template('/index.html', website_name=website_name)


@app.route('/urls', methods=['POST'])
def add_website():
    result = add_website_view(request)
    if result['status'] == 'error':
        flash('Некорректный URL', 'error')
        return render_template('/index.html', website_name=result['website_data']), 422
    elif result['status'] == 'success':
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url_data', id=result['id']))
    elif result['status'] == 'not success':
        flash('Страница уже существует', 'not success')
        return redirect(url_for('get_url_data', id=result['id']))
    
    '''
    if request.method == 'POST':
        website_data = request.form.to_dict()
        website_url = normalize_url(website_data['url'])
        if type(validators.url(website_url)) != bool or len(website_url) > 255:
            flash('Некорректный URL', 'error')
            return render_template('/index.html',
                                   website_name=website_data), 422
        else:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            try:
                create_date = date.today()
                cur.execute("INSERT INTO urls (name, created_at) "
                            "VALUES (%s, %s)", (website_url, create_date))
                conn.commit()
                cur.execute(f"SELECT urls.id, urls.name, urls.created_at, "
                            f"url_checks.id, url_checks.status_code, "
                            f"url_checks.h1, url_checks.title, "
                            f"url_checks.description, "
                            f"url_checks.created_at "
                            f"FROM urls LEFT JOIN url_checks "
                            f"ON urls.id = url_checks.url_id WHERE "
                            f"urls.name = '{website_url}' "
                            f"ORDER BY url_checks.id DESC;")
                result = cur.fetchall()
                cur.close()
                conn.close()
                flash('Страница успешно добавлена', 'success')
                return redirect(url_for('get_url_data', id=result[0][0]))
            except Exception:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(f"SELECT urls.id, urls.name, urls.created_at, "
                            f"url_checks.id, url_checks.status_code, "
                            f"url_checks.h1, url_checks.title, "
                            f"url_checks.description, url_checks.created_at "
                            f"FROM urls LEFT JOIN url_checks "
                            f"ON urls.id = url_checks.url_id "
                            f"WHERE urls.name = '{website_url}' "
                            f"ORDER BY url_checks.id DESC;")
                result = cur.fetchall()
                cur.close()
                conn.close()
                flash('Страница уже существует', 'not success')
                return redirect(url_for('get_url_data', id=result[0][0]))
    '''


@app.route('/urls')
def show_urls():
    '''
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT urls.id, urls.name, url_checks.status_code, "
                "MAX(url_checks.created_at) FROM urls "
                "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                "GROUP BY urls.id, url_checks.status_code "
                "ORDER BY urls.id DESC;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    '''
    result = show_urls_view()
    return render_template('/show_all_urls.html', urls=result)


@app.route('/urls/<id>')
def get_url_data(id):
    '''
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT urls.id, urls.name, urls.created_at, "
                f"url_checks.id, url_checks.status_code, "
                f"url_checks.h1, url_checks.title, url_checks.description, "
                f"url_checks.created_at FROM urls "
                f"LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                f"WHERE urls.id = {id} ORDER BY url_checks.id DESC;")
    checks_website_data = cur.fetchall()
    cur.close()
    conn.close()
    '''
    check_website_data = get_url_data_view(id)
    return render_template('/get_url_data.html', check_data=check_website_data)


@app.route('/urls/<id>/checks', methods=['POST'])
def check_url(id):
    result = check_url_view(id)
    if result == 'error':
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url_data', id=id))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_data', id=id))
    '''
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM urls WHERE id = {id}")
    result = cur.fetchall()
    url = result[0][1]
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code != 200:
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('get_url_data', id=id))
        tags = find_tags(response)
        title = tags['title']
        h1 = tags['h1']
        description = tags['description']
        create_date = date.today()
        cur.execute("INSERT INTO url_checks (url_id, status_code, h1, "
                    "title, description, created_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, status_code, h1, title, description, create_date))
        conn.commit()
        cur.close()
        conn.close()
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url_data', id=id))
    except Exception:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url_data', id=id))
    '''


if __name__ == '__main__':
    app.run()
