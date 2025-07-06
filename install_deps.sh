#!/bin/bash

echo "🔧 Установка зависимостей в виртуальном окружении..."

# Получаем путь к скрипту
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

echo "📁 Директория проекта: $SCRIPT_DIR"
echo "🐍 Виртуальное окружение: $VENV_PATH"

# Проверяем наличие виртуального окружения
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Виртуальное окружение не найдено. Создаем..."
    python3 -m venv "$VENV_PATH"
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
"$VENV_PATH/bin/pip" install --upgrade pip

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
"$VENV_PATH/bin/pip" install aiogram aiosqlite python-dotenv

echo "✅ Зависимости установлены!"
echo ""
echo "📋 Для запуска бота используйте:"
echo "  source venv/bin/activate"
echo "  python main.py" 