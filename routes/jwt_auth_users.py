from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

algorithm  = "HS256"
access_token_duration = 1
secret = "462c1edc78e2be416f9dcb9a54969b0fd14371c013413f47d86ee4e18e134831"

router = APIRouter(
    tags=["jwt_auth_users"],
    responses={404: {"Message": "No encontrado"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    user_name: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Hugo_champ": {
        "user_name": "Hugo_champ",
        "full_name": "Hugo Paredez",
        "email": "hugo.paredez@gmail.com",
        "disabled": False,
        "password": "$2a$12$H9jjHPqmKQixVEpS9e8AuOdb/rCRtKBC6sHHDDkdMdTv1thc586Jy"
    },
    "Hugo_champ2": {
        "user_name": "Hugo_champ2",
        "full_name": "Hugo Paredez 2",
        "email": "hugo.paredez@gmail.com",
        "disabled": True,
        "password": "$2a$12$5yq3ej.A4YhoZ31dSPIY5OUXc4v.P1Onv4s6GWSb7VAAXfzgd/Ndq"
    },
}

def search_user_db(user_name: str):
    if user_name in users_db:
        return UserDB(**users_db[user_name])
    
def search_user(user_name: str):
    if user_name in users_db:
        return User(**users_db[user_name])
    
async def auth_user(token: str = Depends(oauth2_scheme)):

    exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}) 
    try:
        user_name = jwt.decode(token, secret, algorithms=[algorithm]).get("sub")
        if user_name is None:
            raise exeption

    except JWTError:
         raise exeption  
    
    return search_user(user_name)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {
        "sub": user.user_name,
        "exp": datetime.utcnow () + timedelta(minutes=access_token_duration)
    }
    return {"access_token": jwt.encode(access_token, secret, algorithm=algorithm), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user