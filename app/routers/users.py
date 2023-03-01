from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from ..schemas.schema import UserCreate, UserBase, Token, User
from ..db.db import get_session

from datetime import timedelta

from sqlmodel import Session

from ..crud import crud_user
from .dependencies import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"Description": "Not found"}}
)


@router.post("/", response_model=UserBase)
def create_user(input: UserCreate, session: Session = Depends(get_session)):
    user = crud_user.create(input, session)
    return user


@router.get("/me/", response_model=User)
def read_users_me(user: User = Depends(get_current_user)):
    return user


@router.get("/{user_id}/", response_model=UserBase)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud_user.get_user(user_id, session)
    return user


# def read_users_by_email(email: str, session: Session = Depends(get_session)):
#     me = crud_user.get_user_by_email(session=session, email=email)
#     if me:
#         return {"email": me.email, "username": me.username}
#     return HTTPException(status_code=400, detail="User does not exist")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)
                                 ):
    user: UserBase = crud_user.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud_user.create_access_token(
        data={"sub": user.username}, # type: ignore
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

