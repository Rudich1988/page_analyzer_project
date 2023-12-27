import os
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from page_analyzer.adding_website import add_website_view
from page_analyzer.db import check_url_view, get_all_urls, get_url_data_view

app = Flask(__name__)


load_dotenv()
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def show_form():
    website_name = {'url': ''}
    return render_template('/index.html', website_name=website_name)


@app.route('/urls', methods=['GET', 'POST'])
def add_website():
    if request.method == 'POST':
        result = add_website_view(request)
        if result['status'] == 'error':
            flash('Некорректный URL', 'error')
            return (render_template('/index.html',
                                    website_name=result['website_data']),
                    HTTPStatus.UNPROCESSABLE_ENTITY)
        elif result['status'] == 'success':
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_url_data', id=result['id']))
        elif result['status'] == 'not success':
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
    result = check_url_view(id)
    if result == 'error':
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url_data', id=id))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_data', id=id))


if __name__ == '__main__':
    app.run()
