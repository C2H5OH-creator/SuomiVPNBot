#!/bin/bash

echo "🔍 Диагностика проблем с установкой зависимостей..."

# Проверяем версию Python
echo "🐍 Версия Python:"
python3 --version

# Проверяем pip
echo "📦 Версия pip:"
pip --version

# Проверяем виртуальное окружение
echo "🔧 Виртуальное окружение:"
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Активировано: $VIRTUAL_ENV"
else
    echo "❌ Не активировано"
fi

# Проверяем системные зависимости
echo "🔧 Проверяем системные зависимости..."
for pkg in python3-dev build-essential libssl-dev libffi-dev pkg-config gcc g++ make; do
    if dpkg -l | grep -q "^ii  $pkg"; then
        echo "✅ $pkg установлен"
    else
        echo "❌ $pkg НЕ установлен"
    fi
done

# Получаем путь к виртуальному окружению
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

# Активируем виртуальное окружение
if [ -d "$VENV_PATH" ]; then
    echo "🔧 Активируем виртуальное окружение: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    export VIRTUAL_ENV="$VENV_PATH"
    export PATH="$VENV_PATH/bin:$PATH"
    unset PYTHONHOME
else
    echo "❌ Виртуальное окружение не найдено в $VENV_PATH"
    exit 1
fi

# Пробуем установить каждую зависимость отдельно
echo "📦 Тестируем установку зависимостей в виртуальном окружении..."

echo "1. Устанавливаем aiogram..."
if "$VENV_PATH/bin/pip" install aiogram; then
    echo "✅ aiogram установлен успешно"
else
    echo "❌ Ошибка установки aiogram"
fi

echo "2. Устанавливаем aiosqlite..."
if "$VENV_PATH/bin/pip" install aiosqlite; then
    echo "✅ aiosqlite установлен успешно"
else
    echo "❌ Ошибка установки aiosqlite"
fi

echo "3. Устанавливаем python-dotenv..."
if "$VENV_PATH/bin/pip" install python-dotenv; then
    echo "✅ python-dotenv установлен успешно"
else
    echo "❌ Ошибка установки python-dotenv"
fi

echo "🔍 Диагностика завершена!" 