import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent

load_dotenv()

app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

try:
    from .data_base import (
        add_url, get_url_by_id, get_url_by_name, 
        get_all_urls, add_url_check, get_url_checks
    )
    from .normalize_url import normalize_url, validate_url
    from .checker import check_website, CheckError
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    raise


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
    except Exception:
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


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url_data = get_url_by_id(id)
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('urls'))
    
    try:
        # Получаем URL из данных базы
        
        url_name = url_data[1]  # Индекс 1 соответствует полю 'name' в БД
        
        # Выполняем настоящую проверку сайта
        check_data = check_website(url_name)
        
        # Сохраняем проверку с реальными данными
        add_url_check(
            url_id=id,
            status_code=check_data['status_code'],
            h1=check_data['h1'],
            title=check_data['title'],
            description=check_data['description']
        )
        
        flash('Страница успешно проверена', 'success')
        
    except CheckError as e:
        # Обрабатываем ошибки проверки
        flash(str(e), 'danger')
    except Exception:
        # Обрабатываем все остальные ошибки
        flash('Произошла ошибка при проверке', 'danger')
    
    return redirect(url_for('url_detail', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    app.run()