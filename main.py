from fastapi import FastAPI
from data.db import  engine
import models.models as models

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}