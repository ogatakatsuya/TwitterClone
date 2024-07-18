from sqlalchemy import create_engine
from api.models.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}?charset=utf8"
engine = create_engine(DB_URL)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()