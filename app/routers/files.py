from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from .dependencies import S3Dep, get_session, get_current_admin
from ..schemas.schema import File

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
@router.get("/{id}")
def get_file_by_file_id(
    id: int,
    s3: S3Dep = Depends(S3Dep),
    session: Session = Depends(get_session),
    _=Depends(get_current_admin),
):
    q = select(File).where(File.id == id)
    result = session.exec(q).first()
    if result:
        file = s3.get_file(result.s3_object_name)
        if file:
            return FileResponse(file)
    raise HTTPException(status_code=404, detail=f"File with id {id} does not exist")
