from dotenv import load_dotenv
import os

load_dotenv()

# Константы с путём
CHANNEL_ID = os.getenv('CHANNEL_ID')
TOKEN = os.getenv('TOKEN')
TIME_SLEEP = int(os.getenv('TIME_SLEEP'))
MY_TG_ID = int(os.getenv('MY_TG_ID'))
