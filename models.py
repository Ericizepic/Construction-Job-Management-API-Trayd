"""
This module defines the SQLAlchemy ORM models for the application.

Status enum which we use to define possible job statuses

Job class used to define schema for job table. SQLAlchemy automatically maps to the database 
schema and provides methods to perform CRUD operations
"""

from sqlalchemy import Boolean, Column, Integer, String, Date, Enum
from database import Base
import enum

"Status enum which we use to define possible job statuses"
class Status(enum.Enum):
    InProgress = 0
    Completed = 1


"""
Job class used to define schema for job table. SQLAlchemy automatically maps to the database 
schema and provides methods to perform CRUD operations
"""
class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), unique = True)
    customer = Column(String(50))
    startDate = Column(Date)
    endDate = Column(Date)
    status = Column(Enum(Status))
