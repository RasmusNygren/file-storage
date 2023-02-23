from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(
    prefix="/users/",
    tags=["users"],
    responses={404: {"Description": "Not found"}}
)


@router.post("/me/")
def read_users_me(current_user: User = Depends(get_current_user):


