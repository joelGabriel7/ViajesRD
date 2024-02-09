from fastapi import FastAPI
from data.db import  engine
import models.models as models
from api.endpoints.agency.agency_router import router as agency_router
from api.endpoints.category.category_router import router as category_router
from api.endpoints.tourist_place.tourist_place_router import router as tourist_place_router
from api.endpoints.client.client_router import router as client_router  
from api.endpoints.excursions.excursion_router import excursion_router
from api.endpoints.users.users_router import router as users_router

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(category_router)
app.include_router(agency_router)
app.include_router(tourist_place_router)
app.include_router(client_router)
app.include_router(excursion_router)
app.include_router(users_router)

