from fastapi import APIRouter, Depends  #this is used to route the application and its end to another application with which it need sto be integrated 
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext #this is used encryting the data 
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer #req form is used for providing a form type structure where the user can provide the credential and all the ither essential info which will be further used for authencitaion purpose 
from jose import JWTError, jwt #jwt is used for creating the jwt token and jwterror is used for identifying the errors which comes while encrypting and decrytping 
from datetime import timedelta, datetime, timezone 
from fastapi import HTTPException

router = APIRouter(
    prefix="/auth", 
    tags=["auth"] 
)  #poviding the prefix and tags will allow to seperate them in the swagger 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  #this is the secret key which will be used for encryting and decrypting the jwt token 
ALGORITHM = "HS256" #this is the algo followed for the process
 
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #this will be used for creating the token 

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/signin") #this will be used in the dependcy injection func which will be used for authenticationg the reqs,,,,**as we have put a prefix the endpoint for sigin also gets changed from sign to auth/signin


class CreateUserRequet(BaseModel): #this is used for validating the data which we want to add into the user tabel 
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):  #this model is followed for providing the output whenever there is a sucessfull authentication 
    access_token: str
    token_type: str

#db dependency
def get_db():  #this is db dependency  this is used to open a session of the db whenever a certain req for the db comes, then after execting it automatically closes the session 
    db = SessionLocal()
    try:
        yield db    #only code before yield is executed 
    finally: #then it is executed 
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]  #this will be used in every end point it exectues the functionality stated above automatically when called 

def authenticate_user(db: db_dependency, username: str, password: str):   #this function is used for athenticationg the user 
    user = db.query(Users).filter(Users.username == username).one_or_none() #it searches the db fo the record with the same usernamr 
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password): #this verifies the hashed user password with currently typed password by hashibg and matching it  
        return False
    return user #ut returns the user, the user cotains the whole row of the db with all the columns 



def create_acces_token(data: dict, user_id: int, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({'sub': str(user_id), 'id': user_id})
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: Missing user ID")
        return {"id": user_id, "username": payload.get('sub')}
    except JWTError as e:
        print(f"JWT decoding error: {e}")  # Debugging: log the error
        raise HTTPException(status_code=401, detail="Could not validate credentials")



@router.post("/signup")  #this api is used for signup, or registering the user into the db 
def create_user(db: db_dependency, create_user_request: CreateUserRequet): #it taakes the db as teh dependy injection, and createusereqiest for vaildation 
    create_user_model = Users(
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role
    )

    db.add(create_user_model)
    db.commit()
    return "Sign Up Succesfull"
    
@router.post("/signin") #this is used for signin of the already registered user 
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency): #here Oauth2form is used for taking the credentials and sending them for authentication 
    user = authenticate_user(db, form_data.username, form_data.password) #the data from the form is passed here for authentication 
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate User")
    token_data = {"username": user.username}  # Use a dictionary for data
    token = create_acces_token(token_data, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}



#installs 
# 1. pip install python-multipart
# 2. pip install sqlite3
# 3. pip install bcrypt==4.0.1
# 4. pip install passlib
# 5, pip install "python-jose[cryptography]"