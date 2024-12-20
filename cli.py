from database import Session, engine
from models import Flight, Seat, Booking

def add_flight(session, flight_name, departure, destination, date, time):
    """Add a new flight to the database."""
    flight = Flight(
        flight_name=flight_name,
        departure=departure,
        destination=destination,
        date=date,
        time=time,
    )
    session.add(flight)
    session.commit()
    print("Flight added successfully.")

def view_flights(session):
    """View all available flights."""
    flights = session.query(Flight).all()
    if flights:
        for flight in flights:
            print(f"ID: {flight.flight_id}, Name: {flight.flight_name}, From: {flight.departure} To: {flight.destination}, Date: {flight.date}, Time: {flight.time}")
    else:
        print("No flights available.")

def add_seats(session, flight_id, class_type, price, count):
    """Add seats for a given flight."""
    flight = session.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        print(f"Flight with ID {flight_id} not found.")
        return
    
    for _ in range(count):
        seat = Seat(
            flight_id=flight_id,
            class_type=class_type,
            status="available",  # Default status is "available"
            price=price
        )
        session.add(seat)
    
    session.commit()
    print(f"{count} seats added to flight {flight_id}.")

def book_ticket(session, flight_id, class_type, passenger_name, contact_info):
    """Book a ticket for a passenger."""
    flight = session.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        print(f"Flight with ID {flight_id} not found.")
        return

    # Find the first available seat in the specified class
    seat = session.query(Seat).filter(
        Seat.flight_id == flight_id,
        Seat.class_type == class_type,
        Seat.status == "available"
    ).first()
    if not seat:
        print(f"No available seats in {class_type} class for flight {flight_id}.")
        return

    # Create a booking
    booking = Booking(
        flight_id=flight_id,
        seat_id=seat.seat_id,
        passenger_name=passenger_name,
        contact_info=contact_info,
        class_type=class_type,
        price=seat.price
    )
    seat.status = "booked"  # Update seat status to "booked"
    session.add(booking)
    session.commit()
    print(f"Ticket booked for {passenger_name} on flight {flight_id}, {class_type} class.")

def view_bookings(session):
    """View all bookings."""
    bookings = session.query(Booking).all()
    if bookings:
        for booking in bookings:
            flight = session.query(Flight).filter(Flight.flight_id == booking.flight_id).first()
            seat = session.query(Seat).filter(Seat.seat_id == booking.seat_id).first()
            print(f"Booking ID: {booking.booking_id}, Flight: {flight.flight_name}, "
                  f"Seat Class: {seat.class_type}, Passenger: {booking.passenger_name}, "
                  f"Contact: {booking.contact_info}, Price: {booking.price}")
    else:
        print("No bookings found.")

def delete_unoccupied_seat(session, seat_id):
    """Delete an unoccupied seat."""
    seat = session.query(Seat).filter(Seat.seat_id == seat_id, Seat.status == "available").first()
    if seat:
        session.delete(seat)
        session.commit()
        print(f"Unoccupied seat with ID {seat_id} deleted.")
    else:
        print(f"No unoccupied seat found with ID {seat_id}.")
