import telebot
from dotenv import load_dotenv
from pathlib import Path
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Определение базового каталога проекта
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

SUPPORTED_SITES = {'kinogo.fm': 'https://kinogo.fm/'}

bot = telebot.TeleBot(BOT_TOKEN)


def make_connection():
    return f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    url=make_connection(),
    pool_size=5,
    max_overflow=10,
)

Session = sessionmaker(bind=engine)

CELERY_BROKER_URL = 'redis://redis_watcher:6379'
