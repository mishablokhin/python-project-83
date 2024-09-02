import os
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
    make_response
)
from .db import (
    open_connection,
    close_connection,
    is_url_already_exists,
    add_new_url_to_db,
    get_all_urls,
    get_url_info_by_id,
    add_url_check,
    get_url_checks_by_id,
    get_latest_url_check,
    get_url_name_by_id,
    get_url_id_by_name
)
from .utilities import (
    is_valid_url,
    normalize_url,
    make_request_to_url,
    get_site_html_content,
    parse_site
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Главная страница
@app.get('/')
def show_main_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


# Страница со всеми добавленными в БД адресами сайтов
@app.get('/urls')
def show_added_urls_page():
    conn = open_connection()
    urls = get_all_urls(conn)
    urls_latest_check = get_latest_url_check(conn)
    return render_template('urls.html', urls=urls, checks=urls_latest_check)


# Страница с подробностями о конкретном адресе
@app.get('/urls/<id>')
def show_url_info(id):
    conn = open_connection()
    url_info = get_url_info_by_id(conn, id)
    url_checks_info = get_url_checks_by_id(conn, id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url_info=url_info,
                           checks=url_checks_info, messages=messages)


# Обработчик формы добавления нового сайта для проверки
@app.post('/urls')
def add_new_url():
    url = request.form.to_dict()['url']
    if is_valid_url(url):
        normalized_url = normalize_url(url)
        conn = open_connection()
        if is_url_already_exists(conn, normalized_url):
            existing_url_id = get_url_id_by_name(conn, normalized_url)
            flash('Страница уже существует', 'alert-info')
            return redirect(url_for('show_url_info', id=existing_url_id))
        else:
            added_url_id = add_new_url_to_db(conn, normalized_url)
            close_connection(conn)
            flash('Страница успешно добавлена', 'alert-success')
            return redirect(url_for('show_url_info', id=added_url_id))
    else:
        flash('Некорректный URL', 'alert-danger')
        response = make_response(show_main_page())
        response.status_code = 422
        return response


# Обработчик формы запуска проверки для сайта
@app.post('/urls/<id>/check')
def check_url(id):
    conn = open_connection()
    url_name = get_url_name_by_id(conn, id)
    if make_request_to_url(url_name) == 200:
        url_html = get_site_html_content(url_name)
        site_data = parse_site(url_html)
        h1, title, description = site_data['h1'], \
            site_data['title'], \
            site_data['description']
        add_url_check(conn, id, h1, title, description)
        flash('Страница успешно проверена', 'alert-success')
    else:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('show_url_info', id=id))
