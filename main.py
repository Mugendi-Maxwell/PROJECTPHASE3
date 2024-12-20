from database import initialize_db, Session
from cli import add_flight, add_seats, book_ticket, view_flights, view_bookings, delete_unoccupied_seat, update_booking

def main_menu():
    """Main menu for the ticket management system."""
    with Session() as session:
        while True:
            print("\nMain Menu:")
            print("1. Add Flight")
            print("2. Add Seats")
            print("3. Book Ticket")
            print("4. View Flights")
            print("5. View Bookings")
            print("6. Delete Unoccupied Seat")
            print("7. Update Booking")  
            print("8. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                flight_name = input("Flight Name: ")
                departure = input("Departure Location: ")
                destination = input("Destination Location: ")
                date = input("Date (YYYY-MM-DD): ")
                time = input("Time (HH:MM): ")
                add_flight(session, flight_name, departure, destination, date, time)
            elif choice == "2":
                flight_id = int(input("Flight ID: "))
                class_type = input("Class (Economy/Business/First): ")
                price = float(input("Price: "))
                count = int(input("Number of Seats: "))
                add_seats(session, flight_id, class_type, price, count)
            elif choice == "3":
                flight_id = int(input("Flight ID: "))
                class_type = input("Class (Economy/Business/First): ")
                passenger_name = input("Passenger Name: ")
                contact_info = input("Contact Info: ")
                book_ticket(session, flight_id, class_type, passenger_name, contact_info)
            elif choice == "4":
                view_flights(session)
            elif choice == "5":
                view_bookings(session)
            elif choice == "6":
                seat_id = int(input("Seat ID to delete: "))
                delete_unoccupied_seat(session, seat_id)
            elif choice == "7":  # New option to update booking
                booking_id = int(input("Booking ID to update: "))
                new_passenger_name = input("New Passenger Name (Leave blank to keep current): ").strip() or None
                new_contact_info = input("New Contact Info (Leave blank to keep current): ").strip() or None
                new_class_type = input("New Ticket Class (Economy/Business/First, Leave blank to keep current): ").strip() or None
                update_booking(session, booking_id, new_passenger_name, new_contact_info, new_class_type)
            elif choice == "8":
                print("Exiting system.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    initialize_db()
    main_menu()
