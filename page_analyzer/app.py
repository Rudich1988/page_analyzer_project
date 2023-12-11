from flask import Flask, render_template, request, flash, redirect, url_for
import validators
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date

from page_analyzer.correct_url import normalize_url

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


app = Flask(__name__)

app.secret_key = "secret_key"


@app.route('/')
def show_form():
    website_name = {'url': ''}
    return render_template('/index.html', website_name=website_name)


@app.route('/urls', methods=['POST'])
def add_website():
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
                cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                            (website_url, create_date))
                conn.commit()
                cur.execute(f"SELECT * FROM urls WHERE name = '{website_url}'")
                result = cur.fetchall()
                cur.close()
                conn.close()
                flash('Страница успешно добавлена', 'success')
                return render_template('/get_url_data.html', url=result)
            except Exception:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM urls WHERE name = '{website_url}'")
                result = cur.fetchall()
                cur.close()
                conn.close()
                flash('Страница уже существует', 'error')
                return render_template('/get_url_data.html', url=result)


@app.route('/urls')
def show_urls():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls ORDER BY id DESC;")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('/show_all_urls.html', urls=result)


@app.route('/urls/<id>')
def get_url_data(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM urls WHERE id = {id}")
    result = cur.fetchall()
    print(result[0][2])
    cur.execute(f"SELECT id, created_at FROM url_checks WHERE url_id={id} ORDER BY id DESC;")
    checks_website_data = cur.fetchall()
    print(checks_website_data)
    cur.close()
    conn.close()
    return render_template('/get_url_data.html',
                           url=result, check_data=checks_website_data)


@app.route('/urls/<id>/checks', methods=['POST'])
def check_url(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    create_date = date.today()
    cur.execute("INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)", (id, create_date))
    conn.commit()
    cur.close()
    conn.close()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_data', id=id))
