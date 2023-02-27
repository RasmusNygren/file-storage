from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from ..schemas.schema import User, UserCreate
from ..db.db import get_session

from sqlalchemy.orm import Session

from ..crud import crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"Description": "Not found"}}
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    pass


@router.post("/create/", response_model=User)
def create_user(input: UserCreate, session: Session = Depends(get_session)):
    user = crud_user.create(input, session)
    return user


@router.get("/{user_id}", response_model=User)
def get_user(user_id, session: Session = Depends(get_session)):
    user = crud_user.get_user(user_id, session)
    return user


# @router.post("/me/")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     pass

@router.get("/me/")
def read_users_by_email(email: str, session: Session = Depends(get_session)):
    me = crud_user.get_user_by_email(db=session, email=email)
    if me:
        return {"email": me.email, "username": me.username}
    return HTTPException(status_code=400, detail="User does not exist")
