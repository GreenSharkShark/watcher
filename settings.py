from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

SUPPORTED_SITES = ['kinogo.fm']

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


def make_connection():
    return f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    url=make_connection(),
    pool_size=5,
    max_overflow=10,
)

Session = sessionmaker(bind=engine)
