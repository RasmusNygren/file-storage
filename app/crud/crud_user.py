from datetime import datetime, timedelta

from passlib.context import CryptContext
from ..schemas.schema import User, UserCreate, Token
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status

from jose import jwt, JWTError

from sqlmodel import Session, select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Do not store the key here, regenerate and move to dotenv file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


def verify_password(plain_password: str, hashed_password: str):
    pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, session: Session):
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


def get_user_by_email(email: str, db: Session) -> User | None:
    q = select(User).where(User.email == email)
    user = db.execute(q).one_or_none()
    if user:
        return user[0]
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def login_for_access_token(username: str, password: str, session: Session):
    user = authenticate_user(username, password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


