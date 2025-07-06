import os
from dotenv import load_dotenv
import json

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
ADMIN_ID = ADMINS = json.loads(os.getenv("ADMINS", "[]"))

