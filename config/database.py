from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
<<<<<<< HEAD

DB_NAME = "health_backend"
PORT = 5432
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"

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
=======
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database credentials
DB_NAME = os.getenv("DB_NAME")
PORT = 5432
HOST = "localhost"
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# Create DB if not exists
def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # connect to default DB to create new one
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
>>>>>>> b7b20c06daffef9fc7587b574d25ecbf85dce315

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()

        if exists:
            print("✅ Database already exists")
        else:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Database '{DB_NAME}' created successfully!")

        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Unable to connect or create the database:", e)

# Run DB creation
create_database()

# SQLAlchemy DB URL
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

<<<<<<< HEAD
=======
# Dependency for DB session
>>>>>>> b7b20c06daffef9fc7587b574d25ecbf85dce315
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db.close()
=======
        db.close()
>>>>>>> b7b20c06daffef9fc7587b574d25ecbf85dce315
