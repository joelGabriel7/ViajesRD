from fastapi import FastAPI
from data.db import  engine
import models.models as models
from api.endpoints.agency.agency_router import router as agency_router
from api.endpoints.category.category_router import router as category_router
from api.endpoints.tourist_place.tourist_place_router import router as tourist_place_router

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(category_router)
app.include_router(agency_router)
app.include_router(tourist_place_router)

