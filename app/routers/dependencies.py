import os

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from ..crud import crud_user

from ..db.db import get_session

from ..schemas.schema import User

from typing import BinaryIO
import boto3

# TODO: The try/except blocks should more defined except catches

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

class S3Dep():
    def __init__(self):
        sess = boto3.Session(profile_name="fastapi-lambda") # Only for dev else boto3.client("s3")
        self.s3 = sess.client("s3")

    def list_buckets(self):
        return self.s3.list_buckets()

    def upload_file(self, title: str):
        # Make the S3 key identifier be the same as the file name
        self.s3.upload_file(title, "my-lambda-fastapi-bucket", title)

    def upload_file_obj(self, file: BinaryIO, title: str)  -> str | None:
        """
        Return True if the upload succeds, else return False
        Returns the s3 object key, None if the upload failed
        """
        # The S3 key identifier be the same as the file name
        s3_object_key = title
        try:
            self.s3.upload_fileobj(file, "my-lambda-fastapi-bucket", s3_object_key)
            return s3_object_key
        except: 
            return None
                

    # TODO: Might have to convert to absolute path to avoids errors in the future
    def get_file(self, object_name: str, filename: str | None = None) -> str | None:
        """
        Returns the new file name.
        """
        if filename is None:
            filename = object_name

        try:
            self.s3.download_file("my-lambda-fastapi-bucket", object_name, filename)
            return filename
        except: 
            return None


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
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


def get_current_admin(user: User = Depends(get_current_user)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin privileges missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_admin:
        raise credentials_exception
    return user

