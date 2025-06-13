import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = (
    f"postgresql://{os.getenv('CLEVER_USER')}:{os.getenv('CLEVER_PASSWORD')}"
    f"@{os.getenv('CLEVER_HOST')}:{os.getenv('CLEVER_PORT')}/{os.getenv('CLEVER_DATABASE')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()