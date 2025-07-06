#!/bin/bash

# Скрипт для создания systemd сервиса с правильными путями

# Получаем текущую директорию
CURRENT_DIR="$(pwd)"
echo "📁 Текущая директория: $CURRENT_DIR"

# Создаем systemd сервис с правильными путями
cat > systemd/vpnbot.service << EOF
[Unit]
Description=VPN Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd сервис создан с путями:"
echo "   WorkingDirectory: $CURRENT_DIR"
echo "   ExecStart: $CURRENT_DIR/venv/bin/python $CURRENT_DIR/main.py" 