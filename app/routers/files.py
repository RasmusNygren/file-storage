from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from .dependencies import S3Dep
from ..db.db import get_session
from ..schemas.schema import File, Item

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"Description": "Not found"}}
)

@router.post("/uploadfile/")
def upload_file(file: UploadFile, title: str | None = None, s3: S3Dep = Depends(S3Dep), session: Session = Depends(get_session)):
    assert (file and file.filename), "Invalid file"
    if not title:
        title = file.filename
    s3_object_name = s3.upload_file_obj(file.file, title)
    if s3_object_name:
        # Create the File entry 
        new_file = File(s3_object_name=s3_object_name)
        # Flush to gain the auto-assigned id of the new File entry
        session.add(new_file)
        session.flush()

        # Create the Item entry and link the new File entry id.
        new_item = Item(title=file.filename, file_id=new_file.id)
        session.add(new_item)
        session.commit()
        return {"Message": "File Upload Succeded"}

    # There might a better status code to use here
    return HTTPException(status_code=400, detail="File upload failed")

# TODO: This should have query parameter validation
@router.get("/getfile/")
def get_file(file: str, s3: S3Dep = Depends(S3Dep)):
    filename = s3.get_file(file)
    if filename:
        return FileResponse(filename)

    return HTTPException(status_code=404, detail="File does not exist")
