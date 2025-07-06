from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import ADMINS

def get_main_keyboard(user_id=None) -> ReplyKeyboardMarkup:
    """Главная клавиатура с ЛК и Админ панелью"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Личный кабинет'))
    
    if user_id and user_id in ADMINS:
        builder.add(KeyboardButton(text='Админ панель'))
    
    # Настраиваем расположение: по 2 кнопки в ряд
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def get_lk_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура личного кабинета"""
    builder = ReplyKeyboardBuilder()
    # Первая строка: Подписка, Подключиться, ← Назад
    builder.row(
        KeyboardButton(text='Подписка'),
        KeyboardButton(text='Поключиться'),
        KeyboardButton(text='← Назад')
    )
    # Вторая строка: Сообщить о проблеме, ping, ← Назад
    builder.row(
        KeyboardButton(text='Сообщить о проблеме'),
        KeyboardButton(text='ping'),
        KeyboardButton(text='← Назад')
    )
    return builder.as_markup(resize_keyboard=True)

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура админ панели"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Пользователи'))
    builder.add(KeyboardButton(text='Жалобы'))
    builder.add(KeyboardButton(text='📢 Оповещение'))
    builder.add(KeyboardButton(text='← Назад'))
    
    # По 2 кнопки в ряд, кнопка "Назад" справа во всю высоту
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


