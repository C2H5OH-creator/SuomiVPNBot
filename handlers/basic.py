from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_main_keyboard, get_lk_keyboard, get_admin_keyboard
from utils.db import add_or_update_user, add_complaint, get_all_complaints, delete_complaint
from config import ADMINS

class ComplaintStates(StatesGroup):
    waiting_for_complaint = State()
    waiting_for_reply = State()

class NotificationStates(StatesGroup):
    waiting_for_notification = State()

async def send_complaint_notification(bot, complaint_id: int | None, user_name: str, user_id: int, complaint_text: str | None):
    """Отправляет уведомление о новой жалобе всем администраторам"""
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    notification = f"🆕 НОВАЯ ЖАЛОБА #{complaint_id}\n\n"
    notification += f"👤 От: {user_name}\n"
    notification += f"🆔 ID: {user_id}\n"
    notification += f"📝 Текст: {complaint_text}\n\n"
    notification += "Для просмотра всех жалоб нажмите 'Жалобы' в админ панели."
    
    # Создаем inline клавиатуру с кнопками
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Готово", callback_data=f"complaint_done_{complaint_id}"))
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data=f"complaint_cancel_{complaint_id}"))
    builder.add(InlineKeyboardButton(text="💬 Ответить", callback_data=f"complaint_reply_{complaint_id}_{user_id}"))
    builder.add(InlineKeyboardButton(text="🙈 Скрыть", callback_data=f"complaint_hide_{complaint_id}"))
    builder.adjust(2, 2)  # По 2 кнопки в строке
    
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, notification, reply_markup=builder.as_markup())
        except Exception as e:
            print(f"Не удалось отправить уведомление админу {admin_id}: {e}")

router = Router()
ping_countdown = 0

@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.from_user:
        await add_or_update_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            until="2024-12-31",
            config=None
        )
    
    keyboard = get_main_keyboard(message.from_user.id if message.from_user else None)
    await message.answer(
        f'Привет, {message.chat.first_name}! Я ваш VPN бот.',
        reply_markup=keyboard
    )

@router.message(F.text == 'Личный кабинет')
async def handle_lk_button(message: Message):
    keyboard = get_lk_keyboard()
    await message.answer("Личный кабинет", reply_markup=keyboard)

@router.message(F.text == 'Админ панель')
async def handle_admin_panel_button(message: Message):
    keyboard = get_admin_keyboard()
    await message.answer("Админ панель", reply_markup=keyboard)

@router.message(F.text == '← Назад')
async def handle_back_button(message: Message):
    keyboard = get_main_keyboard(message.from_user.id if message.from_user else None)
    await message.answer("Главное меню", reply_markup=keyboard)

@router.message(F.text == 'Сообщить о проблеме')
async def handle_complaint_button(message: Message, state: FSMContext):
    await state.set_state(ComplaintStates.waiting_for_complaint)
    await message.answer("Опишите вашу проблему. Всё, что вы напишете, будет записано как жалоба.")

@router.message(ComplaintStates.waiting_for_complaint)
async def handle_complaint_text(message: Message, state: FSMContext):
    if message.from_user:
        user_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
        if not user_name:
            user_name = f"Пользователь {message.from_user.id}"
        
        complaint_id = await add_complaint(
            user_id=message.from_user.id,
            user_name=user_name,
            complaint_text=message.text
        )
        
        await message.answer("Спасибо! Ваша жалоба записана.")
        await state.clear()
        
        # Отправляем уведомления администраторам
        await send_complaint_notification(message.bot, complaint_id, user_name, message.from_user.id, message.text)
    else:
        await message.answer("Ошибка при сохранении жалобы.")
        await state.clear()

@router.message(ComplaintStates.waiting_for_reply)
async def handle_reply_media(message: Message, state: FSMContext):
    from utils.db import send_reply_to_user, get_user, get_complaint_by_user_id
    
    data = await state.get_data()
    user_id = data.get('reply_user_id')
    
    if not user_id:
        await message.answer("Ошибка при отправке ответа")
        await state.clear()
        return
    
    # Получаем дату последней жалобы пользователя
    complaint = await get_complaint_by_user_id(user_id)
    complaint_date = complaint[4] if complaint else None  # created_at - 5-й элемент
    
    success = False
    reply_text = None
    media_type = None
    file_id = None
    
    # Обрабатываем разные типы сообщений
    if message.text:
        # Текстовое сообщение
        reply_text = message.text
        success = await send_reply_to_user(message.bot, user_id, reply_text, complaint_date=complaint_date)
        
    elif message.photo:
        # Фото
        file_id = message.photo[-1].file_id
        media_type = "photo"
        reply_text = message.caption
        success = await send_reply_to_user(message.bot, user_id, reply_text, media_type, file_id, complaint_date)
        
    elif message.video:
        # Видео
        file_id = message.video.file_id
        media_type = "video"
        reply_text = message.caption
        success = await send_reply_to_user(message.bot, user_id, reply_text, media_type, file_id, complaint_date)
        
    elif message.document:
        # Документ/файл
        file_id = message.document.file_id
        media_type = "document"
        reply_text = message.caption
        success = await send_reply_to_user(message.bot, user_id, reply_text, media_type, file_id, complaint_date)
        
    elif message.voice:
        # Голосовое сообщение
        file_id = message.voice.file_id
        media_type = "voice"
        reply_text = message.caption
        success = await send_reply_to_user(message.bot, user_id, reply_text, media_type, file_id, complaint_date)
        
    elif message.sticker:
        # Стикер
        file_id = message.sticker.file_id
        media_type = "sticker"
        reply_text = message.caption
        success = await send_reply_to_user(message.bot, user_id, reply_text, media_type, file_id, complaint_date)
        
    else:
        await message.answer("❌ Неподдерживаемый тип сообщения")
        await state.clear()
        return
    
    if success:
        # Получаем имя пользователя для подтверждения
        user = await get_user(user_id)
        if user:
            user_id, first_name, last_name, subscription_until, config_path = user
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            if not full_name:
                full_name = f"Пользователь {user_id}"
            await message.answer(f"✅ Ответ отправлен пользователю {full_name}")
        else:
            await message.answer(f"✅ Ответ отправлен пользователю {user_id}")
    else:
        await message.answer("❌ Не удалось отправить ответ пользователю")
    
    await state.clear()

@router.message(NotificationStates.waiting_for_notification)
async def handle_notification_media(message: Message, state: FSMContext):
    from utils.db import get_all_users, send_notification_to_user
    
    users = await get_all_users()
    users_list = list(users) if users else []
    if not users_list:
        await message.answer("❌ Нет пользователей для отправки оповещения")
        await state.clear()
        return
    
    success_count = 0
    error_count = 0
    notification_text = None
    media_type = None
    file_id = None
    
    # Обрабатываем разные типы сообщений
    if message.text:
        # Текстовое сообщение
        notification_text = message.text
        for user in users_list:
            user_id = user[0]  # Первый элемент - user_id
            success = await send_notification_to_user(message.bot, user_id, notification_text)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    elif message.photo:
        # Фото
        file_id = message.photo[-1].file_id
        media_type = "photo"
        notification_text = message.caption
        for user in users_list:
            user_id = user[0]
            success = await send_notification_to_user(message.bot, user_id, notification_text, media_type, file_id)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    elif message.video:
        # Видео
        file_id = message.video.file_id
        media_type = "video"
        notification_text = message.caption
        for user in users_list:
            user_id = user[0]
            success = await send_notification_to_user(message.bot, user_id, notification_text, media_type, file_id)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    elif message.document:
        # Документ/файл
        file_id = message.document.file_id
        media_type = "document"
        notification_text = message.caption
        for user in users_list:
            user_id = user[0]
            success = await send_notification_to_user(message.bot, user_id, notification_text, media_type, file_id)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    elif message.voice:
        # Голосовое сообщение
        file_id = message.voice.file_id
        media_type = "voice"
        notification_text = message.caption
        for user in users_list:
            user_id = user[0]
            success = await send_notification_to_user(message.bot, user_id, notification_text, media_type, file_id)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    elif message.sticker:
        # Стикер
        file_id = message.sticker.file_id
        media_type = "sticker"
        notification_text = message.caption
        for user in users_list:
            user_id = user[0]
            success = await send_notification_to_user(message.bot, user_id, notification_text, media_type, file_id)
            if success:
                success_count += 1
            else:
                error_count += 1
                
    else:
        await message.answer("❌ Неподдерживаемый тип сообщения")
        await state.clear()
        return
    
    # Отправляем отчет о результатах
    report = f"📢 Оповещение отправлено:\n\n"
    report += f"✅ Успешно: {success_count}\n"
    report += f"❌ Ошибок: {error_count}\n"
    report += f"📊 Всего пользователей: {len(users_list)}"
    
    await message.answer(report)
    await state.clear()

@router.message(F.text == 'ping')
async def handle_ping_button(message: Message):
    global ping_countdown
    if ping_countdown == 69:
        try:
            photo = types.FSInputFile('src/test.jpg')
            await message.answer_photo(photo)
            ping_countdown = 0
        except FileNotFoundError:
            await message.answer("Файл не найден")
    else:
        ping_countdown += 1
        await message.answer('pong')

@router.message(F.text == 'Пользователи')
async def handle_users_button(message: Message):
    from utils.db import get_all_users
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    users = await get_all_users()
    
    if users:
        builder = InlineKeyboardBuilder()
        
        for user in users:
            user_id, first_name, last_name, subscription_until, config_path = user
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            if not full_name:
                full_name = f"Пользователь {user_id}"
            
            builder.add(InlineKeyboardButton(
                text=full_name,
                callback_data=f"user_{user_id}"
            ))
        
        builder.adjust(1)  # По одной кнопке в строке
        await message.answer("Выберите пользователя:", reply_markup=builder.as_markup())
    else:
        await message.answer("Пользователей пока нет.")

@router.message(F.text == 'Жалобы')
async def handle_complaints_button(message: Message):
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    
    complaints = await get_all_complaints()
    
    if complaints:
        for complaint in complaints:
            complaint_id, user_id, user_name, complaint_text, created_at = complaint
            
            # Создаем inline клавиатуру для каждой жалобы
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text="✅ Готово", callback_data=f"complaint_done_{complaint_id}"))
            builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data=f"complaint_cancel_{complaint_id}"))
            builder.add(InlineKeyboardButton(text="💬 Ответить", callback_data=f"complaint_reply_{complaint_id}_{user_id}"))
            builder.adjust(3)  # По 3 кнопки в строке
            
            response = f"📋 Жалоба #{complaint_id}\n\n"
            response += f"👤 От: {user_name}\n"
            response += f"🆔 ID: {user_id}\n"
            response += f"📝 Текст: {complaint_text}\n"
            response += f"📅 Дата: {created_at}"
            
            await message.answer(response, reply_markup=builder.as_markup())
    else:
        await message.answer("Жалоб пока нет.")

@router.message(F.text == '📢 Оповещение')
async def handle_notification_button(message: Message, state: FSMContext):
    await state.set_state(NotificationStates.waiting_for_notification)
    await message.answer(
        "📢 Отправьте оповещение для всех пользователей:\n\n"
        "Поддерживаются: текст, фото, видео, файлы, голосовые сообщения и стикеры"
    )

@router.callback_query(lambda c: c.data.startswith('user_'))
async def handle_user_callback(callback_query):
    from utils.db import get_user
    
    user_id = int(callback_query.data.split('_')[1])
    user = await get_user(user_id)
    
    if user:
        user_id, first_name, last_name, subscription_until, config_path = user
        full_name = f"{first_name or ''} {last_name or ''}".strip()
        if not full_name:
            full_name = "Не указано"
        
        response = f"Информация о пользователе:\n\n"
        response += f"ID: {user_id}\n"
        response += f"Имя: {full_name}\n"
        response += f"Подписка активна до: {subscription_until}\n"
        response += f"Конфиг: {config_path or 'Не создан'}"
        
        await callback_query.message.answer(response)
    else:
        await callback_query.message.answer("Пользователь не найден.")
    
    await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith('complaint_'))
async def handle_complaint_callback(callback_query, state: FSMContext):
    data = callback_query.data.split('_')
    action = data[1]
    complaint_id = int(data[2])
    
    if action == "done":
        # Удаляем жалобу из БД
        await delete_complaint(complaint_id)
        await callback_query.message.edit_text(
            callback_query.message.text + "\n\n✅ ОТМЕЧЕНО КАК ВЫПОЛНЕНО"
        )
        await callback_query.answer("Жалоба отмечена как выполненная и удалена из БД")
        
    elif action == "cancel":
        # Удаляем жалобу из БД
        await delete_complaint(complaint_id)
        await callback_query.message.edit_text(
            callback_query.message.text + "\n\n❌ ОТМЕНЕНО"
        )
        await callback_query.answer("Жалоба отменена и удалена из БД")
        
    elif action == "reply":
        user_id = int(data[3])
        await state.update_data(reply_user_id=user_id)
        await state.set_state(ComplaintStates.waiting_for_reply)
        await callback_query.answer("Введите ответ пользователю")
        await callback_query.message.answer(
            f"Отправьте ответ для пользователя {user_id}:\n\n"
            "Поддерживаются: текст, фото, видео, файлы, голосовые сообщения и стикеры"
        )
        
    elif action == "hide":
        # Удаляем сообщение, но не жалобу из БД
        await callback_query.message.delete()
        await callback_query.answer("Уведомление скрыто")
