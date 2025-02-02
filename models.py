"""
This module defines the SQLAlchemy ORM models for the application.

Status enum which we use to define possible job statuses

Job class used to define schema for job table. SQLAlchemy automatically maps to the database 
schema and provides methods to perform CRUD operations

Worker class used to define schema for job table. SQLAlchemy automatically maps to the database 
schema and provides methods to perform CRUD operations
"""

from sqlalchemy import Boolean, Column, Integer, String, Date, Enum
from database import Base
import enum

class Status(enum.Enum):
    InProgress = 0
    Completed = 1


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), unique=False)
    customer = Column(String(50), unique=False)
    startDate = Column(Date)
    endDate = Column(Date)
    status = Column(Enum(Status))


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), unique=False)
    role = Column(String(50), unique=False)
    jobId = Column(Integer)