from sqlalchemy import Column, Integer, String

from app.db import Base


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    age = Column(Integer, nullable=True)
    address = Column(String, nullable=True)
    work = Column(String, nullable=True)
