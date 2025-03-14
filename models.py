from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Courses(Base):
    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)