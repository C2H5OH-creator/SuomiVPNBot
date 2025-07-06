import aiosqlite
import datetime 

DB_PATH = 'vpn_bot.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                subscription_until DATE,
                config_path TEXT
            );
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                complaint_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        ''')
        await db.commit()

async def add_or_update_user(user_id: int, first_name: str | None, last_name: str | None, until: str, config: str | None = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO users (user_id, first_name, last_name, subscription_until, config_path)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                subscription_until=excluded.subscription_until,
                config_path=excluded.config_path;
        ''', (user_id, first_name, last_name, until, config))
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row

async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            return rows

async def add_complaint(user_id: int, user_name: str, complaint_text: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('''
            INSERT INTO complaints (user_id, user_name, complaint_text)
            VALUES (?, ?, ?)
        ''', (user_id, user_name, complaint_text))
        await db.commit()
        return cursor.lastrowid

async def get_all_complaints():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM complaints ORDER BY created_at DESC') as cursor:
            rows = await cursor.fetchall()
            return rows

async def send_reply_to_user(bot, user_id: int, reply_text: str | None = None, media_type: str | None = None, file_id: str | None = None, complaint_date: str | None = None):
    """Отправляет ответ пользователю (текст или медиа)"""
    try:
        if media_type and file_id:
            # Отправляем медиа с подписью
            if complaint_date:
                caption = f"📩 Ответ на вашу жалобу от {complaint_date}:\n\n{reply_text}" if reply_text else f"📩 Ответ на вашу жалобу от {complaint_date}"
            else:
                caption = f"📩 Ответ на вашу жалобу:\n\n{reply_text}" if reply_text else "📩 Ответ на вашу жалобу"
            
            if media_type == "photo":
                await bot.send_photo(user_id, file_id, caption=caption)
            elif media_type == "video":
                await bot.send_video(user_id, file_id, caption=caption)
            elif media_type == "document":
                await bot.send_document(user_id, file_id, caption=caption)
            elif media_type == "voice":
                await bot.send_voice(user_id, file_id, caption=caption)
            elif media_type == "sticker":
                await bot.send_sticker(user_id, file_id)
                if reply_text:
                    if complaint_date:
                        await bot.send_message(user_id, f"📩 Ответ на вашу жалобу от {complaint_date}:\n\n{reply_text}")
                    else:
                        await bot.send_message(user_id, f"📩 Ответ на вашу жалобу:\n\n{reply_text}")
        else:
            # Отправляем только текст
            if complaint_date:
                await bot.send_message(user_id, f"📩 Ответ на вашу жалобу от {complaint_date}:\n\n{reply_text}")
            else:
                await bot.send_message(user_id, f"📩 Ответ на вашу жалобу:\n\n{reply_text}")
        
        return True
    except Exception as e:
        print(f"Не удалось отправить ответ пользователю {user_id}: {e}")
        return False

async def delete_complaint(complaint_id: int):
    """Удаляет жалобу из базы данных"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('DELETE FROM complaints WHERE id = ?', (complaint_id,))
        await db.commit()

async def get_complaint_by_user_id(user_id: int):
    """Получает последнюю жалобу пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT * FROM complaints 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row

async def send_notification_to_user(bot, user_id: int, notification_text: str | None = None, media_type: str | None = None, file_id: str | None = None):
    """Отправляет уведомление пользователю"""
    try:
        if media_type and file_id:
            # Отправляем медиа с подписью
            caption = f"📢 ВАЖНОЕ ОПОВЕЩЕНИЕ\n\n{notification_text}" if notification_text else "📢 ВАЖНОЕ ОПОВЕЩЕНИЕ"
            
            if media_type == "photo":
                await bot.send_photo(user_id, file_id, caption=caption)
            elif media_type == "video":
                await bot.send_video(user_id, file_id, caption=caption)
            elif media_type == "document":
                await bot.send_document(user_id, file_id, caption=caption)
            elif media_type == "voice":
                await bot.send_voice(user_id, file_id, caption=caption)
            elif media_type == "sticker":
                await bot.send_sticker(user_id, file_id)
                if notification_text:
                    await bot.send_message(user_id, f"📢 ВАЖНОЕ ОПОВЕЩЕНИЕ\n\n{notification_text}")
        else:
            # Отправляем только текст
            await bot.send_message(user_id, f"📢 ВАЖНОЕ ОПОВЕЩЕНИЕ\n\n{notification_text}")
        
        return True
    except Exception as e:
        print(f"Не удалось отправить уведомление пользователю {user_id}: {e}")
        return False

