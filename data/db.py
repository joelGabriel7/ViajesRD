from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

# DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:joel1234@localhost/viajes"
#SQLALCHEMY_DATABASE_URL = "postgresql://viajesuser:9r6eTzoadNBtICB05iecXq0jjGv8FK6L@dpg-cnhk6ifsc6pc73dvpmmg-a.oregon-postgres.render.com/viajes_wyl5"
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

