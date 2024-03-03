from fastapi import FastAPI
from data.db import  engine
import models.models as models
from api.endpoints.agency.agency_router import router as agency_router
from api.endpoints.category.category_router import router as category_router
from api.endpoints.tourist_place.tourist_place_router import router as tourist_place_router
from api.endpoints.client.client_router import router as client_router  
from api.endpoints.excursions.excursion_router import excursion_router
from api.endpoints.users.users_router import router as users_router
from api.endpoints.reservation.reservation_router import router as reservation_router
from api.endpoints.payments.paypal_payment import app as paypal_payment
from api.endpoints.payments.payments_list import router as payments_list
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.mount("/static", StaticFiles(directory="static/images"), name="static")


app.include_router(category_router)
app.include_router(agency_router)
app.include_router(tourist_place_router)
app.include_router(client_router)
app.include_router(excursion_router)
app.include_router(users_router)
app.include_router(reservation_router)
# app.include_router(paypal_payment)
app.include_router(payments_list)

