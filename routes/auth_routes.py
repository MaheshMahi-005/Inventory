from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate,UserResponse,Token
from auth import hash_password,create_token,verify_password,get_current_user
import models
router = APIRouter(prefix='/auth',tags=['Authentication'])


@router.post('/register',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    username = user.username.strip().lower()
    existing = db.query(models.User).filter(models.User.username == username).first()
    if existing:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail='username already exist')
    new_user = models.User(username = username,password = hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login',response_model=Token)
def login(form:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    username = form.username.strip().lower()
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect username or password')
    token = create_token({'sub':user.username,'role':user.role})
    return {'access_token':token,'token_type':'bearer'}

@router.get('/me',response_model=UserResponse)
def get_me(current_user:models.User = Depends(get_current_user)):
    return current_user