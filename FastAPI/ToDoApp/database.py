from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db'   #it is the connection string which is used for db connection 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)  #this is used to execute the queries

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)   #this is used to make a connection session between the user and the db

Base = declarative_base() #this is basically the class which are inherited by the model classes to create the tables inside the db