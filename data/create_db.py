from sqlalchemy import create_engine
from db import SQLALCHEMY_DATABASE_URL, Base  # Asegúrate de que la ruta sea correcta
# from models.models import *

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
