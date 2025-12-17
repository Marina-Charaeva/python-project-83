### Hexlet tests and linter status:
[![Actions Status](https://github.com/Marina-Charaeva/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Marina-Charaeva/python-project-83/actions)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Marina-Charaeva_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Marina-Charaeva_python-project-83)

Page Analyzer – это сайт, который выполняет SEO-анализ указанного сайта.

Задеплоенное приложение -> https://python-project-83-sxgw.onrender.com

### Предварительные требования:
- Python 3.11+;
- Pip version 24.2;
- PostgreSQL 13+;

### Установка и запуск:

1. Клонируйте репозиторий.
```
git clone https://github.com/Marina-Charaeva/python-project-83
cd python-project-83
```

2. Настройте зависимости.
```
make install
```

3. Настройте базу данных.
```
sudo -u postgres createdb {databasename}
sudo -u postgres psql -d {databasename} -f database.sql
```

4. Настройте переменные окружения.
Создайте в директории page_analyzer .env файл для переменных окружения со следующей информацией:
DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{databasename}
SECRET_KEY='{your secret key}'

5. Запустите приложение.
```
make dev
```

Приложение будет доступно по адресу: http://localhost:5000