"""
This module sets up the database connection using SQLAlchemy. 
It loads environment variables for database credentials, configures the database engine, and initializes session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_DBNAME = os.getenv("DB_DBNAME")


URL_DATABASE = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DBNAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

