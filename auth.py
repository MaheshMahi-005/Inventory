from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from dotenv import load_dotenv
import models,os

load_dotenv()

#-----password hashing-----
pwd_context  =  CryptContext(schemes=['bcrypt'],deprecated = 'auto')


def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str,hashed:str) -> bool:
    return pwd_context.verify(plain,hashed)


secret_key = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
EXPIRE_TIME = 30

def create_token(data:dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME)
    payload.update({"exp":expire})
    return jwt.encode(payload,secret_key,algorithm=ALGORITHM)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(token:str = Depends(oauth2_schema),db:Session = Depends(get_db)):
    credentials_exceptions =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or Expired Token",headers={'WWW-Authenticate':'Bearer'})
    try:
        payload = jwt.decode(token,secret_key,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exceptions
    return user

def get_current_admin(current_user:models.User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Admin privileges required')
    return current_user