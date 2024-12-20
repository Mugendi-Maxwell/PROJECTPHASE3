import sqlite3
from datetime import datetime

#  Database Setup 
def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect("ticket_management.db")

def initialize_db():
    """Initialize the database tables for Flights, Seats, and Bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_name TEXT NOT NULL,
            departure TEXT NOT NULL,
            destination TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER NOT NULL,
            class TEXT NOT NULL CHECK(class IN ('Economy', 'Business', 'First')),
            status TEXT NOT NULL CHECK(status IN ('available', 'booked')),
            price REAL NOT NULL,
            FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            flight_id INTEGER NOT NULL,
            seat_id INTEGER NOT NULL,
            class TEXT NOT NULL,
            price REAL NOT NULL,
            booking_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
            FOREIGN KEY (seat_id) REFERENCES Seats(seat_id)
        )
        """)

#  Flight Management 
def add_flight(flight_name, departure, destination, date, time):
    """Add a new flight to the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Flights (flight_name, departure, destination, date, time)
        VALUES (?, ?, ?, ?, ?)
        """, (flight_name, departure, destination, date, time))
        print("Flight added successfully.")

def view_flights():
    """Display all flights."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Flights")
        flights = cursor.fetchall()
        if flights:
            print("\nAvailable Flights:")
            for flight in flights:
                print(f"ID: {flight[0]}, Name: {flight[1]}, From: {flight[2]} To: {flight[3]}, Date: {flight[4]}, Time: {flight[5]}")
        else:
            print("No flights available.")

# === Seat Management ===
def add_seats(flight_id, ticket_class, price, count):
    """Add seats to a flight."""
    with connect_db() as conn:
        cursor = conn.cursor()
        for _ in range(count):
            cursor.execute("""
            INSERT INTO Seats (flight_id, class, status, price)
            VALUES (?, ?, 'available', ?)
            """, (flight_id, ticket_class, price))
        print(f"{count} {ticket_class} class seats added to flight ID {flight_id}.")

def delete_unoccupied_seat(seat_id):
    """Delete an unoccupied seat from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM Seats WHERE seat_id = ? AND status = 'available'
        """, (seat_id,))
        if cursor.rowcount > 0:
            print("Seat deleted successfully.")
        else:
            print("Seat deletion failed or the seat is already booked.")

#  Booking Management 
def book_ticket(flight_id, ticket_class, passenger_name, contact_info):
    """Book a ticket for a passenger."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT seat_id, price FROM Seats
        WHERE flight_id = ? AND class = ? AND status = 'available'
        LIMIT 1
        """, (flight_id, ticket_class))
        seat = cursor.fetchone()

        if not seat:
            print("No available seats in this class.")
            return

        seat_id, price = seat
        cursor.execute("""
        INSERT INTO Bookings (passenger_name, contact_info, flight_id, seat_id, class, price)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (passenger_name, contact_info, flight_id, seat_id, ticket_class, price))
        cursor.execute("UPDATE Seats SET status = 'booked' WHERE seat_id = ?", (seat_id,))
        print(f"Ticket booked successfully! Seat ID: {seat_id}, Price: {price}")

def view_bookings():
    """View all bookings."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT B.booking_id, B.passenger_name, B.contact_info, F.flight_name, B.class, B.price, B.booking_time
        FROM Bookings B
        JOIN Flights F ON B.flight_id = F.flight_id
        """)
        bookings = cursor.fetchall()
        if bookings:
            print("\nBookings:")
            for booking in bookings:
                print(f"Booking ID: {booking[0]}, Name: {booking[1]}, Contact: {booking[2]}, Flight: {booking[3]}, Class: {booking[4]}, Price: {booking[5]}, Time: {booking[6]}")
        else:
            print("No bookings found.")

# === CLI Interface ===
def main_menu():
    """Main menu for the ticket management system."""
    while True:
        print("\nMain Menu:")
        print("1. Add Flight")
        print("2. Add Seats")
        print("3. Book Ticket")
        print("4. View Flights")
        print("5. View Bookings")
        print("6. Delete Unoccupied Seat")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            flight_name = input("Flight Name: ")
            departure = input("Departure Location: ")
            destination = input("Destination Location: ")
            date = input("Date (YYYY-MM-DD): ")
            time = input("Time (HH:MM): ")
            add_flight(flight_name, departure, destination, date, time)
        elif choice == "2":
            flight_id = int(input("Flight ID: "))
            ticket_class = input("Class (Economy/Business/First): ")
            price = float(input("Price: "))
            count = int(input("Number of Seats: "))
            add_seats(flight_id, ticket_class, price, count)
        elif choice == "3":
            flight_id = int(input("Flight ID: "))
            ticket_class = input("Class (Economy/Business/First): ")
            passenger_name = input("Passenger Name: ")
            contact_info = input("Contact Info: ")
            book_ticket(flight_id, ticket_class, passenger_name, contact_info)
        elif choice == "4":
            view_flights()
        elif choice == "5":
            view_bookings()
        elif choice == "6":
            seat_id = int(input("Seat ID to delete: "))
            delete_unoccupied_seat(seat_id)
        elif choice == "7":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

# === Program Entry Point ===
if __name__ == "__main__":
    initialize_db()
    main_menu()
