from datetime import datetime, timedelta

from passlib.context import CryptContext
from ..schemas.schema import User, UserCreate, Token
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlmodel import Session, select
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


JWT_ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, session: Session) -> User | bool:
    user = get_user_by_username(username, session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create(obj: UserCreate, session: Session) -> User:
    db_obj = User(
        email = obj.email,
        password = get_password_hash(obj.password),
        username = obj.username,
    )
    session.add(db_obj)
    session.commit()
    return db_obj


def get_user(id: int, session: Session) -> User | None:
    q = select(User).where(User.id == id)
    user = session.execute(q).one_or_none()
    if user:
        return user[0]
    return None


def get_user_by_username(username: str, session: Session) -> User | None:
    q = select(User).where(User.username == username)
    user = session.execute(q).one_or_none()
    if user:
        return user[0]
    return None


def get_user_by_email(email: str, session: Session) -> User | None:
    q = select(User).where(User.email == email)
    user = session.execute(q).one_or_none()
    if user:
        return user[0]
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ["JWT_SECRET_KEY"], algorithm=JWT_ALGORITHM)
    return encoded_jwt

