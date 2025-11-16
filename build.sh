#!/usr/bin/env bash
set -e
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
source $HOME/.local/bin/env
make install
psql -a -d $DATABASE_URL -f database.sql