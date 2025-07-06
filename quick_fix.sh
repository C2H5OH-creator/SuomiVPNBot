#!/bin/bash

echo "🚀 Быстрое исправление проблем с pip..."

# Удаляем поврежденное виртуальное окружение
echo "🗑️  Удаляем поврежденное виртуальное окружение..."
rm -rf venv

# Создаем новое виртуальное окружение
echo "🐍 Создаем новое виртуальное окружение..."
python3 -m venv venv

# Устанавливаем права доступа
echo "🔐 Устанавливаем права доступа..."
chmod -R 755 venv

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

# Обновляем pip через python -m pip
echo "📦 Обновляем pip..."
venv/bin/python -m pip install --upgrade pip

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
venv/bin/python -m pip install aiogram aiosqlite python-dotenv

echo "✅ Готово! Теперь можно запускать бота:"
echo "  source venv/bin/activate"
echo "  python main.py" 