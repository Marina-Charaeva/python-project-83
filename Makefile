install:
	uv sync
dev:
	uv run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
# эта команда запускает веб-сервер по адресу *http://localhost:8000*,
# если в переменных окружения не указан порт, необходимый для деплоя

make lint:
	poetry run flake8 page_analyzer

build:
	./build.sh