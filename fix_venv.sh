#!/bin/bash

echo "🔧 Исправление проблем с виртуальным окружением..."

# Получаем путь к скрипту
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

echo "📁 Директория проекта: $SCRIPT_DIR"
echo "🐍 Виртуальное окружение: $VENV_PATH"

# Удаляем поврежденное виртуальное окружение
if [ -d "$VENV_PATH" ]; then
    echo "🗑️  Удаляем поврежденное виртуальное окружение..."
    rm -rf "$VENV_PATH"
fi

# Проверяем наличие python3-venv
echo "🔍 Проверяем наличие python3-venv..."
if ! dpkg -l | grep -q python3-venv; then
    echo "📦 Устанавливаем python3-venv..."
    apt update
    apt install -y python3-venv
fi

# Создаем новое виртуальное окружение
echo "🐍 Создаем новое виртуальное окружение..."
python3 -m venv "$VENV_PATH"

# Проверяем создание
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Не удалось создать виртуальное окружение!"
    exit 1
fi

# Устанавливаем правильные права доступа
echo "🔐 Устанавливаем права доступа..."
chmod -R 755 "$VENV_PATH"

# Проверяем наличие pip
echo "🔍 Проверяем наличие pip..."
if [ ! -f "$VENV_PATH/bin/pip" ]; then
    echo "❌ pip не найден в виртуальном окружении!"
    echo "🔧 Пробуем переустановить виртуальное окружение..."
    rm -rf "$VENV_PATH"
    python3 -m venv "$VENV_PATH" --clear
fi

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source "$VENV_PATH/bin/activate"

# Проверяем активацию
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Не удалось активировать виртуальное окружение!"
    echo "🔧 Пробуем альтернативный способ..."
    export VIRTUAL_ENV="$VENV_PATH"
    export PATH="$VENV_PATH/bin:$PATH"
    unset PYTHONHOME
fi

echo "✅ Виртуальное окружение активировано: $VIRTUAL_ENV"

# Обновляем pip
echo "📦 Обновляем pip..."
"$VENV_PATH/bin/python" -m pip install --upgrade pip

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
"$VENV_PATH/bin/python" -m pip install aiogram aiosqlite python-dotenv

echo "✅ Виртуальное окружение исправлено и зависимости установлены!"
echo ""
echo "📋 Для запуска бота используйте:"
echo "  source venv/bin/activate"
echo "  python main.py" 