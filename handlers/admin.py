from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from filters.is_admin import IsAdmin

router = Router()

@router.message(F.text == "admin", IsAdmin())
async def admin_button(message: Message):
    await message.answer("У вас есть админские права 👍")
