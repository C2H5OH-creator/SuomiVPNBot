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

# Пробуем установить каждую зависимость отдельно
echo "📦 Тестируем установку зависимостей..."

echo "1. Устанавливаем aiogram..."
if pip install aiogram; then
    echo "✅ aiogram установлен успешно"
else
    echo "❌ Ошибка установки aiogram"
fi

echo "2. Устанавливаем aiosqlite..."
if pip install aiosqlite; then
    echo "✅ aiosqlite установлен успешно"
else
    echo "❌ Ошибка установки aiosqlite"
fi

echo "3. Устанавливаем python-dotenv..."
if pip install python-dotenv; then
    echo "✅ python-dotenv установлен успешно"
else
    echo "❌ Ошибка установки python-dotenv"
fi

echo "🔍 Диагностика завершена!" 