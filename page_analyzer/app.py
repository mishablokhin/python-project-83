import os
from validators import ValidationError
import requests
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash
)
from .db import (
    add_new_url_to_db,
    get_all_urls,
    get_url_info_by_id,
    add_url_check,
    get_url_checks_by_id,
    get_latest_url_check,
    get_url_name_by_id,
    get_url_id_if_exists
)
from .utilities import (
    is_valid_url,
    normalize_url,
    get_seo_information_from_page
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Главная страница
@app.get('/')
def show_main_page():
    return render_template('index.html')


# Страница со всеми добавленными в БД адресами сайтов
@app.get('/urls')
def show_added_urls_page():
    urls = get_all_urls()
    checks = get_latest_url_check()
    checks_dict = {check.url_id: check for check in checks}
    return render_template('urls.html', urls=urls, checks=checks_dict)


# Страница с подробностями о конкретном адресе
@app.get('/urls/<id>')
def show_url_info(id):
    url_info = get_url_info_by_id(id)
    url_checks_info = get_url_checks_by_id(id)
    return render_template('url.html',
                           url_info=url_info, checks=url_checks_info)


# Обработчик формы добавления нового сайта для проверки
@app.post('/urls')
def add_new_url():
    url = request.form.to_dict()['url']
    try:
        if is_valid_url(url):
            normalized_url = normalize_url(url)
            existing_url = get_url_id_if_exists(normalized_url)
            if existing_url:
                flash('Страница уже существует', 'alert-info')
                return redirect(url_for('show_url_info',
                                        id=existing_url))
            else:
                added_url_id = add_new_url_to_db(normalized_url)
                flash('Страница успешно добавлена', 'alert-success')
                return redirect(url_for('show_url_info', id=added_url_id))
        else:
            flash('Некорректный URL', 'alert-danger')
            return render_template('index.html'), 422
    except ValidationError:
        flash('Ошибка валидации URL', 'alert-danger')
        return render_template('index.html'), 422


# Обработчик формы запуска проверки для сайта
@app.post('/urls/<id>/check')
def check_url(id):
    url_name = get_url_name_by_id(id)
    try:
        response = requests.get(url_name)
        status_code = response.status_code
        if status_code == 200:
            html_content = response.text
            site_data = get_seo_information_from_page(html_content)

            h1, title, description = site_data['h1'], \
                site_data['title'], \
                site_data['description']
            add_url_check(id, status_code, h1, title, description)
            flash('Страница успешно проверена', 'alert-success')
        else:
            flash('Произошла ошибка при проверке', 'alert-danger')
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('show_url_info', id=id))
