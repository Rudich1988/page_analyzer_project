import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.db import (get_all_urls, get_url_checks, get_url_id,
                              insert_url, get_url_name, insert_url_checks,
                              get_website_data)
from page_analyzer.url_utils import normalize_url, is_url_valid
from page_analyzer.enums import Statuses
from page_analyzer.find_tags import find_tags


app = Flask(__name__)


load_dotenv()
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def show_form():
    return render_template('/index.html')


@app.get('/urls')
def show_all_urls():
    return render_template('/show_all_urls.html', urls=get_all_urls())


@app.post('/urls')
def add_website():
    website_data = request.form.to_dict()
    website_url = normalize_url(website_data['url'])
    if not is_url_valid(website_url):
        result = {'website_data': website_data,
                  'status': Statuses.ERROR.value}
        flash('Некорректный URL', Statuses.ERROR.value)
        return (render_template('/index.html',
                                web_name=result['website_data']['url']),
                HTTPStatus.UNPROCESSABLE_ENTITY)
    try:
        result = insert_url(website_url)
    except Exception:
        flash('Страница уже существует', Statuses.NOT_SUCCESS.value)
        id = get_url_id(website_url)
        return redirect(url_for('get_url_data',
                        id=id))
    flash('Страница успешно добавлена', Statuses.SUCCESS.value)
    return redirect(url_for('get_url_data',
                    id=result['id']))


@app.route('/urls/<int:id>')
def get_url_data(id):
    try:
        website_data = get_website_data(id)
        check_data = get_url_checks(id)
        return render_template('/get_url_data.html',
                               check_data=check_data, website_data=website_data)
    except Exception:
        return render_template('/error.html')


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url = get_url_name(id)
    try:
        response = requests.get(url)
        status_code = response.status_code
        tags = find_tags(url)
        insert_url_checks(id, status_code, tags['title'],
                          tags['h1'], tags['description'])
        flash('Страница успешно проверена', Statuses.SUCCESS.value)
    except Exception:
        flash('Произошла ошибка при проверке', Statuses.ERROR.value)
    return redirect(url_for('get_url_data', id=id))


if __name__ == '__main__':
    app.run()
