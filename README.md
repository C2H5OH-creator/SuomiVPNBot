# VPN Telegram Bot

Telegram-бот для управления VPN сервисом с системой жалоб, уведомлений и админ-панелью.

## 🚀 Быстрый запуск на сервере

### 1. Подготовка сервера

```bash
# Обновляем систему
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
apt install -y python3 python3-pip python3-venv git
```

### 2. Клонирование проекта

```bash
cd /root
git clone <ваш_репозиторий> VPNbot_dev
cd VPNbot_dev
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
nano .env
```

Добавьте следующие строки:

```env
TELEGRAM_BOT_API_TOKEN=ваш_токен_бота_от_BotFather
ADMINS=[ваш_telegram_id]
```

**Как получить токен бота:**
1. Напишите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен

**Как узнать свой Telegram ID:**
1. Напишите @userinfobot в Telegram
2. Он покажет ваш ID

### 4. Автоматический деплой

```bash
# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем автоматический деплой
./deploy.sh
```

### 5. Ручной запуск (альтернатива)

Если автоматический деплой не подходит:

```bash
# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем бота
python main.py
```

## 📋 Управление ботом

### Через systemd (рекомендуется)

```bash
# Проверить статус
systemctl status vpnbot.service

# Остановить бота
systemctl stop vpnbot.service

# Запустить бота
systemctl start vpnbot.service

# Перезапустить бота
systemctl restart vpnbot.service

# Посмотреть логи
journalctl -u vpnbot.service -f
```

### Автозапуск при перезагрузке

```bash
# Включить автозапуск
systemctl enable vpnbot.service

# Отключить автозапуск
systemctl disable vpnbot.service
```

## 🔧 Структура проекта

```
VPNbot_dev/
├── main.py                 # Главный файл запуска
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости Python
├── .env                  # Переменные окружения
├── bot.log               # Логи бота
├── deploy.sh             # Скрипт автоматического деплоя
├── systemd/
│   └── vpnbot.service    # Systemd сервис
├── handlers/
│   └── basic.py          # Обработчики команд
├── filters/
│   └── is_admin.py       # Фильтр для админов
├── keyboards/
│   └── reply.py          # Клавиатуры
└── utils/
    └── db.py             # Работа с базой данных
```

## 🛠️ Функции бота

### Для пользователей:
- 📋 Личный кабинет
- 🆔 Просмотр своего ID
- 📝 Отправка жалоб
- 📩 Получение ответов на жалобы

### Для администраторов:
- 👥 Управление пользователями
- 📋 Просмотр жалоб
- 💬 Ответы на жалобы
- 📢 Массовые уведомления
- ✅ Отметка жалоб как выполненных

## 🔍 Мониторинг и логи

### Просмотр логов в реальном времени:
```bash
journalctl -u vpnbot.service -f
```

### Просмотр последних логов:
```bash
journalctl -u vpnbot.service -n 50
```

### Просмотр логов за определенный период:
```bash
journalctl -u vpnbot.service --since "2024-01-01" --until "2024-01-02"
```

## 🚨 Устранение неполадок

### Бот не запускается:
1. Проверьте токен в файле `.env`
2. Убедитесь, что все зависимости установлены
3. Проверьте логи: `journalctl -u vpnbot.service -n 20`

### Ошибки с базой данных:
```bash
# Пересоздать базу данных
rm bot.db
systemctl restart vpnbot.service
```

### Проблемы с правами доступа:
```bash
# Исправить права доступа
chown -R root:root /root/VPNbot_dev
chmod -R 755 /root/VPNbot_dev
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи бота
2. Убедитесь в правильности настроек
3. Проверьте подключение к интернету
4. Убедитесь, что токен бота действителен

## 🔄 Обновление бота

```bash
cd /root/VPNbot_dev

# Остановить бота
systemctl stop vpnbot.service

# Обновить код
git pull

# Перезапустить бота
systemctl start vpnbot.service
```
