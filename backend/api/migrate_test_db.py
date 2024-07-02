from sqlalchemy import create_engine
from models.models import Base

DB_URL = "mysql+pymysql://root:rootpassword@test_db:3306/test_data?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()