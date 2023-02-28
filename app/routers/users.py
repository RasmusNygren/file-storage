from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from ..schemas.schema import UserCreate, UserBase
from ..db.db import get_session

from datetime import timedelta
import os

from sqlalchemy.orm import Session

from jose import jwt, JWTError

from ..crud import crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"Description": "Not found"}}
)


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_username(username=username, session=session)
    if user is None:
        raise credentials_exception
    return user



@router.post("/create/", response_model=UserBase)
def create_user(input: UserCreate, session: Session = Depends(get_session)):
    user = crud_user.create(input, session)
    return user


@router.get("/{user_id}/", response_model=UserBase)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud_user.get_user(user_id, session)
    return user


# @router.post("/me/")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     pass

@router.get("/me/", response_model=UserBase)
def read_users_me(user: UserBase = Depends(get_current_user)):
    return user
# def read_users_by_email(email: str, session: Session = Depends(get_session)):
#     me = crud_user.get_user_by_email(session=session, email=email)
#     if me:
#         return {"email": me.email, "username": me.username}
#     return HTTPException(status_code=400, detail="User does not exist")

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = crud_user.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud_user.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

