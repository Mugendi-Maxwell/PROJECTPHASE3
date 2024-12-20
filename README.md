# PROJECTPHASE3
# Ticket Management System

## Overview
The Ticket Management System is a Python-based command-line application for managing flights, seats, and bookings. It uses SQLite for data storage and provides a simple interface for users and administrators to handle ticket-related operations efficiently.

---

## Features
- **Flight Management**: Add and view flights.
- **Seat Management**: Add seats to flights and delete unoccupied seats.
- **Ticket Booking**: Book tickets for available flights and seats.
- **View Bookings**: Display all current bookings with passenger and flight details.
- **Database Storage**: All data is saved in an SQLite database (`ticket_management.db`).

---



## How to Use
1. **Initialize the System**:
   

2. **Main Menu Options**:
   - **Add Flight**: Enter flight details such as name, departure, destination, date, and time.
   - **Add Seats**: Specify the flight ID, class, price, and number of seats.
   - **Book Ticket**: Enter flight ID, class, passenger name, and contact information to book a ticket.
   - **View Flights**: Display all available flights.
   - **View Bookings**: List all ticket bookings with relevant details.
   - **Delete Unoccupied Seat**: Remove seats that are still available.

3. **Exit**: Choose to exit the system safely.

---

## How to Run
1. Clone the repository or copy the script.
2. Run the script using Python:
   ```bash
   python ticket_management.py
   ```
3. Follow the on-screen instructions to use the system.

---

## File Structure
- **`ticket_management.py`**: Main script with the application logic.
- **`ticket_management.db`**: SQLite database file created automatically on the first run.

---

## Future Enhancements
- Add user authentication for admin and passenger roles.
- Include reports for revenue and seat occupancy.
- Implement a graphical user interface (GUI) for better usability.

---

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

Enjoy managing your tickets with ease! 🚀

