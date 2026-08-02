from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PHONE_API_KEY = os.getenv("PHONE_API_KEY")