PORT ?= 8000

install:
	uv sync
dev:
	uv run flask --debug --app page_analyzer:app run --host=0.0.0.0 --port=5000

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
# эта команда запускает веб-сервер по адресу *http://localhost:8000*,
# если в переменных окружения не указан порт, необходимый для деплоя

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

make lint:
	poetry run flake8 page_analyzer

build:
	./build.sh

lint:
	uv run flake8 page_analyzer

test:
	uv run pytest

.PHONY: install dev start render-start build lint test