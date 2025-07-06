#!/bin/bash

# Скрипт для деплоя VPN бота на сервер

echo "🚀 Начинаем деплой VPN бота..."

# Получаем путь к директории скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Директория проекта: $SCRIPT_DIR"

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Устанавливаем..."
    apt update
    apt install -y python3 python3-pip python3-venv
fi

# Переходим в директорию проекта
cd "$SCRIPT_DIR"

# Проверяем наличие необходимых файлов
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден в $SCRIPT_DIR"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ Файл main.py не найден в $SCRIPT_DIR"
    exit 1
fi

# Создаем виртуальное окружение
if [ ! -d "venv" ]; then
    echo "🐍 Создаем виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

# Обновляем pip
echo "📦 Обновляем pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
pip install -r requirements.txt

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📝 Создайте файл .env в директории $SCRIPT_DIR со следующим содержимым:"
    echo "TELEGRAM_BOT_API_TOKEN=ваш_токен_бота"
    echo "ADMINS=[ваш_id_админа]"
    echo ""
    echo "Пример:"
    echo "TELEGRAM_BOT_API_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
    echo "ADMINS=[123456789]"
    exit 1
fi

# Проверяем права на выполнение
chmod +x main.py

# Создаем systemd сервис с правильными путями
echo "🔧 Создаем systemd сервис..."
if [ -f "create_service.sh" ]; then
    chmod +x create_service.sh
    ./create_service.sh
else
    echo "❌ Файл create_service.sh не найден!"
    exit 1
fi

# Копируем systemd сервис
echo "🔧 Копируем systemd сервис..."
cp systemd/vpnbot.service /etc/systemd/system/

# Перезагружаем systemd
systemctl daemon-reload

# Включаем автозапуск
systemctl enable vpnbot.service

# Запускаем сервис
echo "🚀 Запускаем бота..."
systemctl start vpnbot.service

# Проверяем статус
echo "📊 Проверяем статус бота..."
systemctl status vpnbot.service

echo "✅ Деплой завершен!"
echo ""
echo "📋 Полезные команды:"
echo "  systemctl status vpnbot.service  - проверить статус"
echo "  systemctl stop vpnbot.service    - остановить бота"
echo "  systemctl start vpnbot.service   - запустить бота"
echo "  systemctl restart vpnbot.service - перезапустить бота"
echo "  journalctl -u vpnbot.service -f  - смотреть логи в реальном времени" 