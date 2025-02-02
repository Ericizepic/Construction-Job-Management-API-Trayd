from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


username = 'root'
password = 'Du20060318'
host = 'localhost'
database = 'traydJobManagementDb'


URL_DATABASE = f'mysql+pymysql://{username}:{password}@{host}/{database}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

