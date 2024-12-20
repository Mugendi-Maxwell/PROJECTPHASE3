from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_name = Column(String, nullable=False)
    departure = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    date = Column(String, nullable=False)  
    time = Column(String, nullable=False) 

    seats = relationship("Seat", back_populates="flight", cascade="all, delete-orphan")

class Seat(Base):
    __tablename__ = 'seats'
    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), nullable=False)
    class_type = Column(String, CheckConstraint("class_type IN ('Economy', 'Business', 'First')"), nullable=False)
    status = Column(String, CheckConstraint("status IN ('available', 'booked')"), nullable=False, default="available")
    price = Column(Float, nullable=False)  # Price of the seat

    flight = relationship("Flight", back_populates="seats")
    bookings = relationship("Booking", back_populates="seat", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seats.seat_id'), nullable=False)
    class_type = Column(String, nullable=False)  
    booking_time = Column(DateTime, default=datetime.utcnow)

    seat = relationship("Seat", back_populates="bookings")

