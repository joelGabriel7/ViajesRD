from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Date,Enum
from sqlalchemy.orm import relationship
from data.db import Base
from sqlalchemy import func

class TouristPlace(Base):

    __tablename__ = 'tourist_places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String(length=255))
    image = Column(String)
    location = Column(String)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship("Categories", back_populates="tourist_places")
    excursions = relationship("Excursions", back_populates="tourist_place")
    images = relationship("TouristPlaceImage", back_populates="tourist_place")
    
    created = Column(Date, default=func.current_date())
    updated = Column(Date, default=func.current_date())


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
    legal_registration_number = Column(String(length=255),unique=True, nullable=False)
    license_number = Column(String(length=255), unique=True, nullable=False)
    license_expiration_date = Column(Date(), default=func.current_date())
    certications = Column(String(length=255))
    insurance_number = Column(String(length=255))
    insurance_provider = Column(String(length=255))
    legal_contact_name = Column(String(length=255))

    status = Column(Enum('active', 'inactive', name='status'), default='active')


    excursions = relationship("Excursions", back_populates="agency")  # Cambiado de 'agencies' a 'agency'
    # Cambiado de 'user' a 'users'

    
    created_at = Column(Date(), default=func.current_date())
    updated_at = Column(Date(), default=func.current_date())

class Reservations(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    
    date_reservation = Column(Date(), default=func.current_date())
    number_of_places = Column(Integer, default=0)
    status = Column(Enum('pending', 'confirmed', 'cancelled', name='status'), default='pending')

    client_id = Column(Integer, ForeignKey('clients.id'))
    excursion_id = Column(Integer, ForeignKey('excursions.id'))

    client = relationship("Clients", back_populates="reservations")  
    excursion = relationship("Excursions", back_populates="reservations")  
    payment = relationship("Payments", back_populates="reservation")

    created = Column(DateTime(), default=func.current_timestamp(), onupdate=func.current_timestamp())
    updated = Column(DateTime(), default=func.current_timestamp(), onupdate=func.current_timestamp())

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

    agency = relationship("Agencies", back_populates="excursions")  # Cambiado de 'agencies' a 'agency'
    tourist_place = relationship("TouristPlace", back_populates="excursions")
    reservations = relationship("Reservations", back_populates="excursion")  # Cambiado de 'reservation' a 'reservations'
    # payments = relationship("Payments", backref="excursion")

    created = Column(DateTime(), default=func.current_date())
    updated = Column(DateTime(), default=func.current_date())
    
class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)
    status = Column(String(length=150), default='pending')
    payment_method = Column(String(length=150), default='cash')
    date_payment = Column(DateTime(), default=func.current_date())
    reservation_id = Column(Integer, ForeignKey('reservations.id'))
    # excursion_id = Column(Integer, ForeignKey('excursions.id'))

    reservation = relationship("Reservations", back_populates="payment")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=150), unique=False, nullable=False)
    hashed_password = Column(String(), nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    status = Column(Enum('active', 'inactive', name='status'), default='active')
    role = Column(Enum('agency', 'client', name='role'), default='user')
    
    created = Column(Date(), default=func.current_date())
    updated = Column(Date(), default=func.current_date())





