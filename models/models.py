from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Date,Enum, Boolean
from sqlalchemy.orm import relationship
from data.db import Base
from sqlalchemy import func

class TouristPlace(Base):

    __tablename__ = 'tourist_places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String(length=255))
    location = Column(String)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Categories", back_populates="tourist_places")
    excursions = relationship("Excursions", back_populates="tourist_place")
    images = relationship("TouristPlaceImage", back_populates="tourist_place")
    ratings = relationship("TouristPlaceRating", back_populates="tourist_place")
    
    created = Column(Date, default=func.current_date())
    updated = Column(Date, default=func.current_date())


class TouristPlaceRating(Base):
    __tablename__ = 'tourist_place_ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    tourist_place_id = Column(Integer, ForeignKey('tourist_places.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    tourist_place = relationship("TouristPlace", back_populates="ratings")
    user = relationship("Users", back_populates="ratings")

class TouristPlaceImage(Base):
    __tablename__ = 'tourist_places_images'
    id = Column(Integer, primary_key = True, index=True)
    image_url = Column(String,  nullable=True)
    tourist_place_id = Column(Integer, ForeignKey("tourist_places.id"), nullable=False)
    tourist_place = relationship("TouristPlace", back_populates="images")

      
class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=150)) 
    last_name = Column(String(length=150))
    birth_date = Column(Date(), default=func.current_date())
    gender = Column(String(length=150))
    phone = Column(String(length=20))
    email = Column(String(length=255))  
    address = Column(String(length=255))
    client_code = Column(String(length=150), unique=True, nullable=False)
    
    users = relationship("Users", back_populates="client")
    reservations = relationship("Reservations", back_populates="client")  # Cambiado de 'reservation' a 'reservations'

    created = Column(Date(), default=func.current_date())
    updated = Column(Date(), default=func.current_date())

class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150))  
    description = Column(String(length=255))
    code_category = Column(String(length=150), unique=True, nullable=False)
    tourist_places = relationship("TouristPlace", back_populates="category")

    created_at = Column(Date(), default=func.current_date())
    updated_at = Column(Date(), default=func.current_date())

class Agencies(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150))  
    description = Column(String(length=255))  
    address = Column(String(length=255))
    phone = Column(String(length=20))
    email = Column(String(length=255)) 
    logo = Column(String(length=255))
    rnc = Column(String(length=255),unique=True, nullable=False)
    status = Column(Enum('active', 'inactive', name='status'), default='active')
    excursions = relationship("Excursions", back_populates="agency") 
    users = relationship("Users", back_populates="agency")     
    created_at = Column(Date(), default=func.current_date())
    updated_at = Column(Date(), default=func.current_date())

class Reservations(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date_reservation = Column(DateTime(), default=func.current_timestamp())
    total_amount = Column(Float, default=0.0)
    client = relationship("Clients", back_populates="reservations")
    reservation_details = relationship("ReservationDetails", back_populates="reservation", cascade="all, delete-orphan")
    payments = relationship("Payments", back_populates="reservation", cascade="all, delete-orphan")

    created_at = Column(DateTime(), default=func.current_timestamp())
    updated_at = Column(DateTime(), default=func.current_timestamp(), onupdate=func.current_timestamp())

class ReservationDetails(Base):
    __tablename__ = 'reservation_details'
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'))
    excursion_id = Column(Integer, ForeignKey('excursions.id'))
    quantity = Column(Integer)
    price = Column(Float)
    status =Column(Integer, default=1)
    
    reservation = relationship("Reservations", back_populates="reservation_details")
    excursion = relationship("Excursions", back_populates="reservation_details")
    



class Excursions(Base):

    __tablename__ = 'excursions'

    id = Column(Integer, primary_key=True, index=True)

    date_excursion  = Column(Date(), default=func.now())
    duration_excursion = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    available_places = Column(Integer, default=0)
    description = Column(String(length=255))
    agency_id = Column(Integer, ForeignKey('agencies.id'))
    tourist_place_id = Column(Integer, ForeignKey('tourist_places.id'))

    agency = relationship("Agencies", back_populates="excursions")  
    tourist_place = relationship("TouristPlace", back_populates="excursions")
    reservation_details = relationship("ReservationDetails", cascade="all, delete-orphan", back_populates="excursion")

    created = Column(DateTime(), default=func.current_date())
    updated = Column(DateTime(), default=func.current_date())
    
class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(255), nullable=False)
    payment_date = Column(DateTime(), default=func.current_timestamp())
    status = Column(Integer, default=1)
    reservation = relationship("Reservations", back_populates="payments")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=150), unique=True, nullable=False)
    hashed_password = Column(String(), nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    status = Column(Enum('active', 'inactive', name='status'), default='active')
    role = Column(Enum('agency', 'client', name='role'), default='user')
    agency_id = Column(Integer, ForeignKey('agencies.id'), nullable=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)

    agency = relationship("Agencies", back_populates="users", uselist=False)
    client = relationship("Clients", back_populates="users", uselist=False)
    ratings = relationship("TouristPlaceRating", back_populates="user")

    created = Column(Date(), default=func.current_date())
    updated = Column(Date(), default=func.current_date())






