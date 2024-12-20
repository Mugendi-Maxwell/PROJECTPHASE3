# ticket_management/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///ticket_management.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def initialize_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)
