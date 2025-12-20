import json
import os
import hashlib
from datetime import datetime

# File paths
USERS_FILE = "users.json"
EVENTS_FILE = "events.json"
BOOKINGS_FILE = "bookings.json"
VENDORS_FILE = "vendors.json"

# Initialize JSON files
def initialize_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(VENDORS_FILE):
        with open(VENDORS_FILE, 'w') as f:
            json.dump([], f)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load and save data
def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# ==================== AUTHENTICATION ====================
def register():
    users = load_data(USERS_FILE)
    print("\n=== REGISTER ===")
    name = input("Enter your name: ").strip()
    username = input("Enter username: ").strip()
    
    # Check if username exists
    if any(u['username'] == username for u in users):
        print("Username already exists!")
        return None
    
    password = input("Enter password: ").strip()
    user_type = input("Register as (user/vendor/admin): ").strip().lower()
    
    if user_type not in ['user', 'vendor', 'admin']:
        print("Invalid user type!")
        return None
    
    new_user = {
        'name': name,
        'username': username,
        'password': hash_password(password),
        'user_type': user_type
    }
    
    users.append(new_user)
    save_data(USERS_FILE, users)
    print(f"Registration successful! Welcome {name}")
    return new_user

def login():
    users = load_data(USERS_FILE)
    print("\n=== LOGIN ===")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    for user in users:
        if user['username'] == username and user['password'] == hash_password(password):
            print(f"Login successful! Welcome {user['name']}")
            return user
    
    print("Invalid credentials!")
    return None

# ==================== DISPLAY FUNCTIONS ====================
def display_events():
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    print("\n" + "="*60)
    print("AVAILABLE EVENTS".center(60))
    print("="*60)
    for i, event in enumerate(events, 1):
        print(f"\n{i}. {event['name']}")
        print(f"   Date: {event['date']}")
        print(f"   Location: {event['location']}")
        print(f"   Ticket Price: ${event['ticket_price']}")
        print(f"   Total Seats: {event['total_seats']}")
        booked = sum(1 for row in event['seat_map'] for seat in row if seat == 'X')
        print(f"   Available Seats: {event['total_seats'] - booked}")
    print("="*60)

def display_seat_map(event):
    print(f"\n=== SEAT MAP FOR {event['name']} ===")
    print("Legend: [ ] = Available, [X] = Booked\n")
    
    seat_map = event['seat_map']
    rows = len(seat_map)
    cols = len(seat_map[0])
    
    # Column headers
    print("    ", end="")
    for col in range(cols):
        print(f" {col+1:2}", end="")
    print("\n")
    
    # Display seats
    for row_idx, row in enumerate(seat_map):
        row_label = chr(65 + row_idx)  # A, B, C...
        print(f"{row_label:2}  ", end="")
        for seat in row:
            if seat == 'X':
                print("[X]", end="")
            else:
                print("[ ]", end="")
        print()

# ==================== USER FUNCTIONS ====================
def user_menu(user):
    while True:
        print(f"\n=== USER MENU ({user['name']}) ===")
        print("1. View All Events")
        print("2. View Event Details")
        print("3. Book a Seat")
        print("4. My Bookings")
        print("5. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            display_events()
        elif choice == '2':
            view_event_details()
        elif choice == '3':
            book_seat(user)
        elif choice == '4':
            view_user_bookings(user)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def view_event_details():
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number to view details: ")) - 1
        if 0 <= event_num < len(events):
            event = events[event_num]
            print(f"\n=== {event['name']} ===")
            print(f"Date: {event['date']}")
            print(f"Location: {event['location']}")
            print(f"Description: {event['description']}")
            print(f"Ticket Price: ${event['ticket_price']}")
            print(f"Total Seats: {event['total_seats']}")
            booked = sum(1 for row in event['seat_map'] for seat in row if seat == 'X')
            print(f"Available Seats: {event['total_seats'] - booked}")
            
            show_map = input("\nView seat map? (y/n): ").strip().lower()
            if show_map == 'y':
                display_seat_map(event)
        else:
            print("Invalid event number!")
    except ValueError:
        print("Invalid input!")

def book_seat(user):
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number to book: ")) - 1
        if 0 <= event_num < len(events):
            event = events[event_num]
            display_seat_map(event)
            
            row_input = input("\nEnter row (A, B, C...): ").strip().upper()
            col_input = int(input("Enter seat number: ")) - 1
            
            row_idx = ord(row_input) - 65
            
            if 0 <= row_idx < len(event['seat_map']) and 0 <= col_input < len(event['seat_map'][0]):
                if event['seat_map'][row_idx][col_input] == 'X':
                    print("Seat already booked!")
                else:
                    # Process payment
                    print(f"\n=== PAYMENT ===")
                    print(f"Event: {event['name']}")
                    print(f"Seat: {row_input}{col_input+1}")
                    print(f"Amount: ${event['ticket_price']}")
                    confirm = input("Confirm payment? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        # Update seat map
                        event['seat_map'][row_idx][col_input] = 'X'
                        save_data(EVENTS_FILE, events)
                        
                        # Create booking
                        bookings = load_data(BOOKINGS_FILE)
                        booking = {
                            'booking_id': f"BK{len(bookings)+1:04d}",
                            'username': user['username'],
                            'event_name': event['name'],
                            'seat': f"{row_input}{col_input+1}",
                            'amount': event['ticket_price'],
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        bookings.append(booking)
                        save_data(BOOKINGS_FILE, bookings)
                        
                        # Display receipt
                        print("\n" + "="*50)
                        print("BOOKING RECEIPT".center(50))
                        print("="*50)
                        print(f"Booking ID: {booking['booking_id']}")
                        print(f"Name: {user['name']}")
                        print(f"Event: {event['name']}")
                        print(f"Date: {event['date']}")
                        print(f"Location: {event['location']}")
                        print(f"Seat: {booking['seat']}")
                        print(f"Amount Paid: ${booking['amount']}")
                        print(f"Booking Time: {booking['date']}")
                        print("="*50)
                        print("Thank you for your booking!")
                        print("="*50)
                    else:
                        print("Payment cancelled.")
            else:
                print("Invalid seat selection!")
        else:
            print("Invalid event number!")
    except (ValueError, IndexError):
        print("Invalid input!")

def view_user_bookings(user):
    bookings = load_data(BOOKINGS_FILE)
    user_bookings = [b for b in bookings if b['username'] == user['username']]
    
    if not user_bookings:
        print("\nNo bookings found.")
        return
    
    print("\n=== MY BOOKINGS ===")
    for booking in user_bookings:
        print(f"\nBooking ID: {booking['booking_id']}")
        print(f"Event: {booking['event_name']}")
        print(f"Seat: {booking['seat']}")
        print(f"Amount: ${booking['amount']}")
        print(f"Date: {booking['date']}")
        print("-" * 40)

# ==================== VENDOR FUNCTIONS ====================
def vendor_menu(user):
    while True:
        print(f"\n=== VENDOR MENU ({user['name']}) ===")
        print("1. View All Events")
        print("2. View Event Stall Details")
        print("3. Book a Stall")
        print("4. My Stall Bookings")
        print("5. Cancel Stall Booking")
        print("6. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            display_events()
        elif choice == '2':
            view_stall_details()
        elif choice == '3':
            book_stall(user)
        elif choice == '4':
            view_vendor_bookings(user)
        elif choice == '5':
            cancel_stall_booking(user)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def view_stall_details():
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number to view stall details: ")) - 1
        if 0 <= event_num < len(events):
            event = events[event_num]
            vendors = load_data(VENDORS_FILE)
            event_vendors = [v for v in vendors if v['event_name'] == event['name']]
            
            print(f"\n=== STALL DETAILS FOR {event['name']} ===")
            print(f"Total Stalls: {event['total_stalls']}")
            print(f"Stall Price: ${event['stall_price']}")
            print(f"Booked Stalls: {len(event_vendors)}")
            print(f"Available Stalls: {event['total_stalls'] - len(event_vendors)}")
        else:
            print("Invalid event number!")
    except ValueError:
        print("Invalid input!")

def book_stall(user):
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number to book stall: ")) - 1
        if 0 <= event_num < len(events):
            event = events[event_num]
            vendors = load_data(VENDORS_FILE)
            event_vendors = [v for v in vendors if v['event_name'] == event['name']]
            
            # Check if vendor already booked
            if any(v['username'] == user['username'] for v in event_vendors):
                print("You have already booked a stall for this event!")
                return
            
            if len(event_vendors) >= event['total_stalls']:
                print("Sorry, all stalls are booked!")
            else:
                print(f"\n=== STALL BOOKING ===")
                print(f"Event: {event['name']}")
                print(f"Stall Price: ${event['stall_price']}")
                confirm = input("Confirm booking? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    vendor_booking = {
                        'booking_id': f"VS{len(vendors)+1:04d}",
                        'username': user['username'],
                        'vendor_name': user['name'],
                        'event_name': event['name'],
                        'stall_number': len(event_vendors) + 1,
                        'amount': event['stall_price'],
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    vendors.append(vendor_booking)
                    save_data(VENDORS_FILE, vendors)
                    
                    # Display receipt
                    print("\n" + "="*50)
                    print("STALL BOOKING RECEIPT".center(50))
                    print("="*50)
                    print(f"Booking ID: {vendor_booking['booking_id']}")
                    print(f"Vendor Name: {user['name']}")
                    print(f"Event: {event['name']}")
                    print(f"Stall Number: {vendor_booking['stall_number']}")
                    print(f"Amount Paid: ${vendor_booking['amount']}")
                    print(f"Booking Time: {vendor_booking['date']}")
                    print("="*50)
                    print("Stall booked successfully!")
                    print("="*50)
                else:
                    print("Booking cancelled.")
        else:
            print("Invalid event number!")
    except ValueError:
        print("Invalid input!")

def view_vendor_bookings(user):
    vendors = load_data(VENDORS_FILE)
    user_bookings = [v for v in vendors if v['username'] == user['username']]
    
    if not user_bookings:
        print("\nNo stall bookings found.")
        return
    
    print("\n=== MY STALL BOOKINGS ===")
    for booking in user_bookings:
        print(f"\nBooking ID: {booking['booking_id']}")
        print(f"Event: {booking['event_name']}")
        print(f"Stall Number: {booking['stall_number']}")
        print(f"Amount: ${booking['amount']}")
        print(f"Date: {booking['date']}")
        print("-" * 40)

def cancel_stall_booking(user):
    vendors = load_data(VENDORS_FILE)
    user_bookings = [v for v in vendors if v['username'] == user['username']]
    
    if not user_bookings:
        print("\nNo stall bookings found.")
        return
    
    print("\n=== CANCEL STALL BOOKING ===")
    for i, booking in enumerate(user_bookings, 1):
        print(f"{i}. Event: {booking['event_name']} - Stall {booking['stall_number']}")
    
    try:
        choice = int(input("\nEnter booking number to cancel: ")) - 1
        if 0 <= choice < len(user_bookings):
            confirm = input("Are you sure you want to cancel? (y/n): ").strip().lower()
            if confirm == 'y':
                cancelled = user_bookings[choice]
                vendors.remove(cancelled)
                save_data(VENDORS_FILE, vendors)
                print("Booking cancelled successfully!")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input!")

# ==================== ADMIN FUNCTIONS ====================
def admin_menu(user):
    while True:
        print(f"\n=== ADMIN MENU ({user['name']}) ===")
        print("1. View All Events")
        print("2. Add New Event")
        print("3. Remove Event")
        print("4. View Event Details (Seats & Vendors)")
        print("5. View All Bookings")
        print("6. View All Vendor Bookings")
        print("7. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            display_events()
        elif choice == '2':
            add_event()
        elif choice == '3':
            remove_event()
        elif choice == '4':
            admin_view_event_details()
        elif choice == '5':
            view_all_bookings()
        elif choice == '6':
            view_all_vendor_bookings()
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def add_event():
    print("\n=== ADD NEW EVENT ===")
    name = input("Event name: ").strip()
    date = input("Event date (YYYY-MM-DD): ").strip()
    location = input("Location: ").strip()
    description = input("Description: ").strip()
    
    try:
        rows = int(input("Number of seat rows: "))
        cols = int(input("Number of seats per row: "))
        ticket_price = float(input("Ticket price: $"))
        total_stalls = int(input("Total stalls for vendors: "))
        stall_price = float(input("Stall price: $"))
        
        # Create seat map
        seat_map = [[' ' for _ in range(cols)] for _ in range(rows)]
        total_seats = rows * cols
        
        new_event = {
            'name': name,
            'date': date,
            'location': location,
            'description': description,
            'ticket_price': ticket_price,
            'total_seats': total_seats,
            'seat_map': seat_map,
            'total_stalls': total_stalls,
            'stall_price': stall_price
        }
        
        events = load_data(EVENTS_FILE)
        events.append(new_event)
        save_data(EVENTS_FILE, events)
        
        print(f"\nEvent '{name}' added successfully!")
    except ValueError:
        print("Invalid input!")

def remove_event():
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events to remove.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number to remove: ")) - 1
        if 0 <= event_num < len(events):
            event_name = events[event_num]['name']
            confirm = input(f"Are you sure you want to remove '{event_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                events.pop(event_num)
                save_data(EVENTS_FILE, events)
                print(f"Event '{event_name}' removed successfully!")
        else:
            print("Invalid event number!")
    except ValueError:
        print("Invalid input!")

def admin_view_event_details():
    events = load_data(EVENTS_FILE)
    if not events:
        print("\nNo events available.")
        return
    
    display_events()
    try:
        event_num = int(input("\nEnter event number: ")) - 1
        if 0 <= event_num < len(events):
            event = events[event_num]
            bookings = load_data(BOOKINGS_FILE)
            vendors = load_data(VENDORS_FILE)
            
            event_bookings = [b for b in bookings if b['event_name'] == event['name']]
            event_vendors = [v for v in vendors if v['event_name'] == event['name']]
            
            print(f"\n=== {event['name']} - ADMIN VIEW ===")
            print(f"Date: {event['date']}")
            print(f"Location: {event['location']}")
            
            print(f"\n--- SEAT INFORMATION ---")
            display_seat_map(event)
            print(f"Total Bookings: {len(event_bookings)}")
            print(f"Revenue from Seats: ${len(event_bookings) * event['ticket_price']}")
            
            print(f"\n--- VENDOR INFORMATION ---")
            print(f"Total Stalls: {event['total_stalls']}")
            print(f"Booked Stalls: {len(event_vendors)}")
            print(f"Revenue from Stalls: ${len(event_vendors) * event['stall_price']}")
            
            if event_vendors:
                print("\nVendor List:")
                for v in event_vendors:
                    print(f"  - {v['vendor_name']} (Stall {v['stall_number']})")
        else:
            print("Invalid event number!")
    except ValueError:
        print("Invalid input!")

def view_all_bookings():
    bookings = load_data(BOOKINGS_FILE)
    if not bookings:
        print("\nNo bookings found.")
        return
    
    print("\n=== ALL SEAT BOOKINGS ===")
    for booking in bookings:
        print(f"\nBooking ID: {booking['booking_id']}")
        print(f"User: {booking['username']}")
        print(f"Event: {booking['event_name']}")
        print(f"Seat: {booking['seat']}")
        print(f"Amount: ${booking['amount']}")
        print(f"Date: {booking['date']}")
        print("-" * 40)

def view_all_vendor_bookings():
    vendors = load_data(VENDORS_FILE)
    if not vendors:
        print("\nNo vendor bookings found.")
        return
    
    print("\n=== ALL VENDOR BOOKINGS ===")
    for vendor in vendors:
        print(f"\nBooking ID: {vendor['booking_id']}")
        print(f"Vendor: {vendor['vendor_name']}")
        print(f"Event: {vendor['event_name']}")
        print(f"Stall: {vendor['stall_number']}")
        print(f"Amount: ${vendor['amount']}")
        print(f"Date: {vendor['date']}")
        print("-" * 40)

# ==================== GUEST FUNCTIONS ====================
def guest_menu():
    while True:
        print("\n=== GUEST MENU ===")
        print("1. View All Events")
        print("2. View Event Details")
        print("3. Book a Seat (Login Required)")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            display_events()
        elif choice == '2':
            view_event_details()
        elif choice == '3':
            print("\nYou need to login or register to book a seat!")
            return 'redirect_login'
        elif choice == '4':
            break
        else:
            print("Invalid choice!")
    return None

# ==================== MAIN MENU ====================
def main():
    initialize_files()
    
    while True:
        print("\n" + "="*50)
        print("EVENT MANAGEMENT SYSTEM".center(50))
        print("="*50)
        print("1. Login")
        print("2. Register")
        print("3. Continue as Guest")
        print("4. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            user = login()
            if user:
                if user['user_type'] == 'user':
                    user_menu(user)
                elif user['user_type'] == 'vendor':
                    vendor_menu(user)
                elif user['user_type'] == 'admin':
                    admin_menu(user)
        
        elif choice == '2':
            register()
        
        elif choice == '3':
            result = guest_menu()
            if result == 'redirect_login':
                continue
        
        elif choice == '4':
            print("\nThank you for using Event Management System!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()