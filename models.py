from sqlalchemy import Boolean, Column, Integer, String, Date, Enum
from database import Base
import enum

class Status(enum.Enum):
    InProgress = 0
    Completed = 1


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50), unique = True)
    customer = Column(String(50))
    startDate = Column(Date)
    endDate = Column(Date)
    status = Column(Enum(Status))
