from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456"
    },
    "Hugo_champ2": {
        "user_name": "Hugo_champ2",
        "full_name": "Hugo Paredez 2",
        "email": "hugo.paredez@gmail.com",
        "disabled": True,
        "password": "654321"
    },
}

def search_user_db(user_name: str):
    if user_name in users_db:
        return UserDB(**users_db[user_name])


def search_user(user_name: str):
    if user_name in users_db:
        return User(**users_db[user_name])


async def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.user_name, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user