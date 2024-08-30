from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field 
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from routers.auth import get_current_user
from fastapi import HTTPException

#this is one of the router which icntains the main part of the code
router = APIRouter()   #fast api application intialization 



class TodoRequest(BaseModel):         #this is used to validate the incoming database data request where it follows the architechture of the db and its retrictions or not before adding to the db 
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)


#db dependency
def get_db():  #this is db dependency  this is used to open a session of the db whenever a certain req for the db comes, then after execting it automatically closes the session 
    db = SessionLocal()
    try:
        yield db    #only code before yield is executed 
    finally: #then it is executed 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]  #this will be used in every end point it exectues the functionality stated above automatically when called 
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/read_all")
async def read_all(db: db_dependency, user: user_dependency):     #dependency injection: it means we need to esecute the thing given under depends() before executing the function
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.post("/add")
async def add_data(db: db_dependency, todo: TodoRequest, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = Todos(**todo.dict(), owner_id=user['id'])  # Corrected: user['id']
    db.add(todo_model)
    db.commit()
    return {"success": True}

@router.put("/update")
async def update_data(db: db_dependency, id: int, todo: TodoRequest,  user: user_dependency):
    todo_model = db.query(Todos).filter(Todos.id == id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        return {"error": "Todo not found"}
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    db.commit()
    return {"success": True}

@router.get("/fetch/{todo_id}")
async def fetch_data(db: db_dependency, todo_id: int, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        return {"error": "Todo not found"}
    return todo_model

@router.delete("/delete/{todo_id}")
async def delete_data(db: db_dependency, todo_id: int, user: user_dependency):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        return {"error": "Todo not found"}
    db.delete(todo_model)
    db.commit()
    return {"success": True}

