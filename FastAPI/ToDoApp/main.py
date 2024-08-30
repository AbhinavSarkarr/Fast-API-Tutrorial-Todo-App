from fastapi import FastAPI
from database import Base, engine
from routers import auth, todos

app = FastAPI()   #fast api application intialization 

Base.metadata.create_all(bind=engine)  #it is used to create the db with the tables given in the model file, once the db with the provided name is created it will not be excuted again

app.include_router(auth.router) #this is used to include other fastapi applications and their end points into this fast api application
app.include_router(todos.router) #this one includes the auth appkication 

#Both the rputer applications are now combined with the main application 



