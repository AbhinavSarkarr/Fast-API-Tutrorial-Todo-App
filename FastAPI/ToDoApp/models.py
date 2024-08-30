from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):    #this is basically used to create the architecture of the table which will be created inside the db and it inherits the base from db file
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(255), nullable=True)

class Todos(Base):    #this is basically used to create the architecture of the table which will be created inside the db and it inherits the base from db file
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    priority = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))






