from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

DB_NAME = "healthnew"
PORT = 5432
HOST = "localhost"
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def create_database():
    try:
        # Connect to the default postgres DB
        conn = psycopg2.connect(
            dbname="postgres",  # must specify this to connect without DB_NAME
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if DB exists (use single quotes for strings in SQL)
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()

        if exists:
            print("Database already exists")
        else:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully!")

        cur.close()
        conn.close()
    except Exception as e:
        print("Unable to connect to the database", e)

# Run the creation function
create_database()

# SQLAlchemy DB URL
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
