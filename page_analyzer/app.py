import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from page_analyzer.logic_views import (
    add_website_view,
    check_url_view,
    get_url_data_view,
    show_urls_view,
)


app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def show_form():
    website_name = {'url': ''}
    return render_template('/index.html', website_name=website_name)


@app.route('/urls', methods=['POST'])
def add_website():
    result = add_website_view(request)
    if result['status'] == 'error':
        flash('Некорректный URL', 'error')
        return render_template('/index.html',
                               website_name=result['website_data']), 422
    elif result['status'] == 'success':
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url_data', id=result['id']))
    elif result['status'] == 'not success':
        flash('Страница уже существует', 'not success')
        return redirect(url_for('get_url_data', id=result['id']))


@app.route('/urls')
def show_urls():
    result = show_urls_view()
    return render_template('/show_all_urls.html', urls=result)


@app.route('/urls/<id>')
def get_url_data(id):
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


if __name__ == '__main__':
    app.run()
