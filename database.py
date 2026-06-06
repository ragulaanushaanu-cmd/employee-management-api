import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. Load the secret variables from the .env file
load_dotenv()

# 2. Grab the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in your .env file!")

print("FINAL DB URL (Loaded from .env):", DATABASE_URL)

# 3. Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TEST CONNECTION 
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DATABASE CONNECTED SUCCESSFULLY:", result.scalar())
except Exception as e:
    print("❌ DATABASE ERROR:", e)