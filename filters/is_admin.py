from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMINS


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False
        return message.from_user.id in ADMINS
