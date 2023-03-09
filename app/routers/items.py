import shortuuid

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlmodel import Session, select

from ..schemas.schema import User, File, Item, ItemUpdateRead
from .dependencies import S3Dep, get_current_user, get_session



router = APIRouter(
    prefix="/items", tags=["items"], responses={404: {"Description": "Not found"}}
)


@router.get("/", response_model=list[Item])
def get_items(
    user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    q = select(Item).where(Item.owner_id == user.id)
    result = session.exec(q).fetchall()
    return result


def _generate_uuid(length: int = 6):
    return shortuuid.uuid()[:length]


@router.post("/")
def upload_item(
    file: UploadFile,
    title: str | None = None,
    s3: S3Dep = Depends(S3Dep),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    assert file and file.filename, "Invalid file"

    if not title:
        title = file.filename
    s3_object_key = f"{_generate_uuid()}/{user.id}/{file.filename}"
    s3_object_key = s3.upload_file_obj(file.file, title, s3_object_key=s3_object_key)
    if s3_object_key:
        # Create the File entry
        new_file = File(s3_object_name=s3_object_key)

        # Flush to gain the auto-assigned id of the new File entry
        session.add(new_file)
        session.flush()
        session.refresh(new_file)

        # Create the Item entry and link the new File entry id.
        new_item = Item(title=title, file_id=new_file.id, owner_id=user.id)
        session.add(new_item)
        session.commit()
        return {"Message": "File Upload Succeded",
                "Item id": new_item.id}

    # There might a better status code to use here
    return HTTPException(status_code=400, detail="File upload failed")


@router.get("/{item_id}")
def get_item(
    item_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    q = select(Item).where(Item.id == item_id, Item.owner_id == user.id)
    result = session.exec(q).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"The item with id {item_id} does not exist or you do not have access")
    return result


@router.post("/setread/")
def set_item_read_status(
        item_update: ItemUpdateRead,
        user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
        ):
    q = select(Item).where(Item.id == item_update.id, Item.owner_id == user.id)
    item = session.exec(q).first()
    item.read = item_update.read
    session.add(item)
    session.commit()    

    return {"Message": "Read status successfully updated",
            "New read status": item_update.read}




