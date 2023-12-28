import os
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from page_analyzer.db import (get_all_urls, get_url_data_view,
                              insert_url, get_url_name, check_url_view)
from page_analyzer.url_utils import normalize_url, is_url_valid
from page_analyzer.enums import Statuses
from page_analyzer.find_tags import find_tags
import requests

app = Flask(__name__)


load_dotenv()
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def show_form():
    return render_template('/index.html')


@app.route('/urls', methods=['GET', 'POST'])
def add_website():
    if request.method == 'POST':
        website_data = request.form.to_dict()
        website_url = normalize_url(website_data['url'])
        if not is_url_valid(website_url):
            result = {'website_data': website_data, 'status': 'error'}
        else:
            result = insert_url(website_url)
        match result['status']:
            case Statuses.ERROR:
                flash('Некорректный URL', 'error')
                return (render_template('/index.html',
                                        web_name=result['website_data']['url']),
                        HTTPStatus.UNPROCESSABLE_ENTITY)
            case Statuses.SUCCESS:
                flash('Страница успешно добавлена', 'success')
                return redirect(url_for('get_url_data', id=result['id']))
            case Statuses.NOT_SUCCESS:
                flash('Страница уже существует', 'not success')
                return redirect(url_for('get_url_data', id=result['id']))
    else:
        result = get_all_urls()
        return render_template('/show_all_urls.html', urls=result)


@app.route('/urls/<int:id>')
def get_url_data(id):
    website_data, check_data = get_url_data_view(id)
    return render_template('/get_url_data.html',
                           check_data=check_data, website_data=website_data)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url = get_url_name(id)
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code != 200:
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('get_url_data', id=id))
        tags = find_tags(url)
        result = check_url_view(id, status_code, tags['title'],
                                tags['h1'], tags['description'])
    except Exception:
        result = Statuses.ERROR
    if result == Statuses.ERROR:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url_data', id=id))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_data', id=id))


if __name__ == '__main__':
    app.run()
