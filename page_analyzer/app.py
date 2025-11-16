import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from .data_base import (
    add_url, get_url_by_id, get_url_by_name, 
    get_all_urls, add_url_check, get_url_checks
)
from .normalize_url import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls():
    urls_list = get_all_urls()
    return render_template('urls.html', urls=urls_list)


@app.route('/urls', methods=['POST'])
def add_url_page():
    url = request.form.get('url', '').strip()
    
    error = validate_url(url)
    if error:
        flash(error, 'danger')
        return render_template('index.html', url=url), 422
    
    normalized_url = normalize_url(url)
    
    existing_url = get_url_by_name(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_detail', id=existing_url[0]))
    
    try:
        url_id = add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url_detail', id=url_id))
    except Exception as e:
        flash('Произошла ошибка при добавлении страницы', 'danger')
        return render_template('index.html', url=url), 422


@app.route('/urls/<int:id>')
def url_detail(id):
    url_data = get_url_by_id(id)
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('urls'))
    
    checks = get_url_checks(id)
    return render_template('url_detail.html', url=url_data, checks=checks)


if __name__ == '__main__':
    app.run()