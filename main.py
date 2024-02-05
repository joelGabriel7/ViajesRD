from fastapi import FastAPI
from data.db import  engine
import models.models as models
from api.endpoints.agency.agency_router import router as agency_router

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(agency_router)

