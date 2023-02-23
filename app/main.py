from fastapi import FastAPI
from mangum import Mangum
import uvicorn
from .routers import files

app = FastAPI()

# Temporary hack to ensure that Base is aware of all the defined models before creating the tables
from .models import file
from .db.db import Base, engine
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine, checkfirst=True)

app.include_router(files.router)

@app.get("/")
def entry():
    return {"Message": "Hello World"}


handler = Mangum(app) # type: ignore

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
