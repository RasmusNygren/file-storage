from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse 
from .dependencies import S3Dep, get_session, get_current_user
from ..schemas.schema import File, User

from sqlmodel import select, Session


router = APIRouter(
    prefix="/files", tags=["files"], responses={404: {"Description": "Not found"}}
)


# @router.get("/")
# def get_file(file: str = Query(title="S3 Object Name"),
#              s3: S3Dep = Depends(S3Dep),
#              user: User = Depends(get_current_admin)
#              ):
#     filename = s3.get_file(file)
#     if filename:
#         return FileResponse(filename)

#     return HTTPException(status_code=404, detail="File does not exist")


# Must be admin endpoint, users retrieve files via item.
@router.get("/{file_id}")
def get_file_by_file_id(
    file_id: int,
    s3: S3Dep=Depends(S3Dep),
    session: Session=Depends(get_session),
    user: User=Depends(get_current_user),
):
    q = select(File).where(File.id == file_id)
    result = session.exec(q).first()
    if result:
        if not result.item.owner_id == user.id and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have access to that file",
                headers={"WWW-Authenticate": "Bearer"},
            )
        file = s3.get_file(result.s3_object_name)
        if file:
            return FileResponse(file)
    raise HTTPException(status_code=404, detail=f"File with id {id} does not exist")

