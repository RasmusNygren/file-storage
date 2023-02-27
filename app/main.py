from fastapi import FastAPI
from mangum import Mangum
import uvicorn
from .routers import files, users
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Temporary hack to ensure that Base is aware of all the defined models before creating the tables
from .schemas import schema
from .db.db import SQLModel, engine
# SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine, checkfirst=True)

app.include_router(files.router)
app.include_router(users.router)

@app.get("/")
def entry():
    return {"Message": "Hello World"}


handler = Mangum(app) # type: ignore

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
