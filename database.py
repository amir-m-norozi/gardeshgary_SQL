import psycopg2

# تنظیمات اتصال به دیتابیس
def get_connection():
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="opsg8113",
        host="localhost",
        port="5432"
    )
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:opsg8113@localhost/postgres"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

