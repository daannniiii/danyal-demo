import os
import json
from datetime import datetime
import random

# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60)

def pause():
    """Pause and wait for user input"""
    input("\nPress Enter to continue...")

# ==================== SEAT MAP CLASS ====================

class SeatMap:
    """Manages seat booking for an event"""
    
    def __init__(self, rows, seats_per_row):
        self.rows = rows
        self.seats_per_row = seats_per_row
        # Create seat map (True = available, False = occupied)
        self.seats = [[True for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}  # {seat_label: {user, time}}
    
    def book_seat(self, row, seat, username):
        """Book a seat for a user"""
        if 0 <= row < self.rows and 0 <= seat < self.seats_per_row:
            if self.seats[row][seat]:
                self.seats[row][seat] = False
                seat_label = f"{row+1}{chr(65+seat)}"
                self.bookings[seat_label] = {
                    "user": username,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return True, seat_label
            else:
                return False, "Seat already occupied"
        return False, "Invalid seat"
    
    def cancel_seat(self, row, seat):
        """Cancel a seat booking"""
        if 0 <= row < self.rows and 0 <= seat < self.seats_per_row:
            if not self.seats[row][seat]:
                self.seats[row][seat] = True
                seat_label = f"{row+1}{chr(65+seat)}"
                if seat_label in self.bookings:
                    del self.bookings[seat_label]
                return True
        return False
    
    def display(self):
        """Display the seat map"""
        print("\n[X] = Occupied  [ ] = Available\n")
        
        # Column headers
        print("   ", end="")
        for i in range(self.seats_per_row):
            print(f"  {chr(65+i)} ", end="")
        print("\n")
        
        # Rows with seats
        for row_idx, row in enumerate(self.seats):
            print(f"{row_idx+1:2d} ", end="")
            for seat_idx, is_available in enumerate(row):
                if seat_idx == self.seats_per_row // 2:
                    print("  ", end="")  # Aisle space
                
                if is_available:
                    print("[ ]", end=" ")
                else:
                    print("[X]", end=" ")
            print()
        print()
    
    def get_available_count(self):
        """Get number of available seats"""
        count = 0
        for row in self.seats:
            count += sum(row)
        return count
    
    def get_total_seats(self):
        """Get total number of seats"""
        return self.rows * self.seats_per_row

# ==================== EVENT CLASS ====================

class Event:
    """Represents an event with seat and vendor management"""
    
    def __init__(self, event_id, name, date, location, price, rows, seats_per_row, vendor_slots):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.location = location
        self.price = price
        self.seat_map = SeatMap(rows, seats_per_row)
        self.total_vendor_slots = vendor_slots
        self.vendor_bookings = {}  # {vendor_username: {status, time, details}}
        self.description = ""
    
    def get_available_vendor_slots(self):
        """Get number of available vendor slots"""
        approved = sum(1 for v in self.vendor_bookings.values() if v['status'] == 'approved')
        return self.total_vendor_slots - approved
    
    def to_dict(self):
        """Convert event to dictionary for saving"""
        return {
            'event_id': self.event_id,
            'name': self.name,
            'date': self.date,
            'location': self.location,
            'price': self.price,
            'rows': self.seat_map.rows,
            'seats_per_row': self.seat_map.seats_per_row,
            'seats': self.seat_map.seats,
            'bookings': self.seat_map.bookings,
            'total_vendor_slots': self.total_vendor_slots,
            'vendor_bookings': self.vendor_bookings,
            'description': self.description
        }
    
    @staticmethod
    def from_dict(data):
        """Create event from dictionary"""
        event = Event(
            data['event_id'],
            data['name'],
            data['date'],
            data['location'],
            data['price'],
            data['rows'],
            data['seats_per_row'],
            data['total_vendor_slots']
        )
        event.seat_map.seats = data['seats']
        event.seat_map.bookings = data['bookings']
        event.vendor_bookings = data['vendor_bookings']
        event.description = data.get('description', '')
        return event

# ==================== DATA MANAGER ====================

class DataManager:
    """Manages all data storage and retrieval"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.events_file = "events.json"
        self.bookings_file = "user_bookings.json"
        
        # Load or initialize data
        self.users = self.load_users()
        self.events = self.load_events()
        self.user_bookings = self.load_user_bookings()
        
        # Create default admin if no users exist
        if not self.users:
            self.users['admin'] = {
                'password': 'admin123',
                'role': 'admin',
                'name': 'Administrator'
            }
            self.save_users()
    
    def load_users(self):
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_events(self):
        """Load events from file"""
        try:
            with open(self.events_file, 'r') as f:
                data = json.load(f)
                return {eid: Event.from_dict(edata) for eid, edata in data.items()}
        except FileNotFoundError:
            return {}
    
    def save_events(self):
        """Save events to file"""
        data = {eid: event.to_dict() for eid, event in self.events.items()}
        with open(self.events_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_user_bookings(self):
        """Load user bookings from file"""
        try:
            with open(self.bookings_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_user_bookings(self):
        """Save user bookings to file"""
        with open(self.bookings_file, 'w') as f:
            json.dump(self.user_bookings, f, indent=2)
    
    def add_user_booking(self, username, event_id, seat_label, ticket_id):
        """Add a booking for a user"""
        if username not in self.user_bookings:
            self.user_bookings[username] = []
        
        self.user_bookings[username].append({
            'ticket_id': ticket_id,
            'event_id': event_id,
            'seat': seat_label,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_user_bookings()

# ==================== AUTHENTICATION ====================

def login(data_manager):
    """Handle user login"""
    print_header("LOGIN")
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    if username in data_manager.users:
        if data_manager.users[username]['password'] == password:
            print(f"\n✅ Login successful! Welcome, {data_manager.users[username]['name']}")
            pause()
            return username, data_manager.users[username]['role']
        else:
            print("\n❌ Incorrect password!")
            pause()
            return None, None
    else:
        print("\n❌ User not found!")
        pause()
        return None, None

def register(data_manager):
    """Handle user registration"""
    print_header("REGISTER")
    
    print("Select role:")
    print("1. User (Book tickets)")
    print("2. Vendor (Book stalls)")
    print("3. Admin (Manage platform)")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        role = 'user'
    elif choice == '2':
        role = 'vendor'
    elif choice == '3':
        role = 'admin'
        # Admin registration requires a secret code
        secret = input("Enter admin secret code: ").strip()
        if secret != "ADMIN2025":
            print("\n❌ Invalid admin code!")
            pause()
            return
        print("✅ Admin code verified!")
    else:
        print("\n❌ Invalid choice!")
        pause()
        return
    
    username = input("\nUsername: ").strip()
    
    if username in data_manager.users:
        print("\n❌ Username already exists!")
        pause()
        return
    
    password = input("Password: ").strip()
    name = input("Full Name: ").strip()
    
    data_manager.users[username] = {
        'password': password,
        'role': role,
        'name': name
    }
    data_manager.save_users()
    
    print(f"\n✅ Registration successful! You can now login as {role}.")
    pause()

# ==================== GUEST MODULE ====================

def guest_mode(data_manager):
    """Guest browsing mode"""
    while True:
        clear_screen()
        print_header("GUEST MODE - FESTIO EVENT PLATFORM")
        
        print("\n1. Browse Events")
        print("2. View Event Details")
        print("3. Login")
        print("4. Register")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            browse_events(data_manager, is_guest=True)
        elif choice == '2':
            view_event_details(data_manager, is_guest=True)
        elif choice == '3':
            username, role = login(data_manager)
            if username:
                return username, role
        elif choice == '4':
            register(data_manager)
        elif choice == '5':
            print("\n👋 Thank you for visiting FESTIO!")
            return None, None
        else:
            print("\n❌ Invalid choice!")
            pause()

def browse_events(data_manager, is_guest=False):
    """Display all events"""
    clear_screen()
    print_header("AVAILABLE EVENTS")
    
    if not data_manager.events:
        print("\n❌ No events available at the moment.")
        pause()
        return
    
    for event_id, event in data_manager.events.items():
        available_seats = event.seat_map.get_available_count()
        total_seats = event.seat_map.get_total_seats()
        
        print(f"\n{'─'*60}")
        print(f"Event ID: {event.event_id}")
        print(f"Name: {event.name}")
        print(f"Date: {event.date}")
        print(f"Location: {event.location}")
        print(f"Price: ${event.price}")
        print(f"Seats Available: {available_seats}/{total_seats}")
        print(f"Vendor Slots Available: {event.get_available_vendor_slots()}/{event.total_vendor_slots}")
    
    print(f"\n{'─'*60}")
    
    if is_guest:
        print("\n💡 Login to book tickets!")
    
    pause()

def view_event_details(data_manager, is_guest=False):
    """View details of a specific event"""
    clear_screen()
    print_header("EVENT DETAILS")
    
    if not data_manager.events:
        print("\n❌ No events available.")
        pause()
        return None
    
    # Show event list
    for event_id in data_manager.events.keys():
        print(f"  {event_id}. {data_manager.events[event_id].name}")
    
    event_id = input("\nEnter Event ID: ").strip()
    
    if event_id not in data_manager.events:
        print("\n❌ Event not found!")
        pause()
        return None
    
    event = data_manager.events[event_id]
    
    clear_screen()
    print_header(f"EVENT: {event.name}")
    print(f"\nDate: {event.date}")
    print(f"Location: {event.location}")
    print(f"Price: ${event.price}")
    print(f"Description: {event.description if event.description else 'No description'}")
    print(f"\n{'─'*60}")
    print(f"Total Seats: {event.seat_map.get_total_seats()}")
    print(f"Available Seats: {event.seat_map.get_available_count()}")
    print(f"Vendor Slots: {event.get_available_vendor_slots()}/{event.total_vendor_slots} available")
    
    if is_guest:
        print("\n💡 Login to book tickets!")
        pause()
        return None
    
    return event_id

# ==================== USER MODULE ====================

def user_dashboard(data_manager, username):
    """User dashboard"""
    while True:
        clear_screen()
        print_header(f"USER DASHBOARD - {data_manager.users[username]['name']}")
        
        print("\n1. Browse Events")
        print("2. Book Ticket")
        print("3. My Bookings")
        print("4. Logout")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            browse_events(data_manager)
        elif choice == '2':
            book_ticket(data_manager, username)
        elif choice == '3':
            view_my_bookings(data_manager, username)
        elif choice == '4':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def book_ticket(data_manager, username):
    """Book a ticket for an event"""
    event_id = view_event_details(data_manager)
    
    if not event_id:
        return
    
    event = data_manager.events[event_id]
    
    if event.seat_map.get_available_count() == 0:
        print("\n❌ Sorry, event is fully booked!")
        pause()
        return
    
    print("\n" + "─"*60)
    print("SEAT MAP")
    print("─"*60)
    event.seat_map.display()
    
    seat_input = input("Enter seat (e.g., 5B): ").strip().upper()
    
    # Parse seat input
    row_str = ""
    seat_letter = ""
    for char in seat_input:
        if char.isdigit():
            row_str += char
        elif char.isalpha():
            seat_letter += char
    
    if not row_str or not seat_letter:
        print("\n❌ Invalid seat format!")
        pause()
        return
    
    row = int(row_str) - 1
    seat = ord(seat_letter) - 65
    
    # Book the seat
    success, message = event.seat_map.book_seat(row, seat, username)
    
    if not success:
        print(f"\n❌ {message}")
        pause()
        return
    
    # Payment simulation
    print("\n" + "─"*60)
    print("PAYMENT")
    print("─"*60)
    print(f"Event: {event.name}")
    print(f"Seat: {message}")
    print(f"Price: ${event.price}")
    
    confirm = input("\nProceed to payment? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        # Cancel the booking
        event.seat_map.cancel_seat(row, seat)
        print("\n❌ Booking cancelled!")
        pause()
        return
    
    # Simulate payment
    print("\nProcessing payment...")
    import time
    time.sleep(2)
    
    # Random payment success (90% success rate for simulation)
    if random.random() < 0.9:
        ticket_id = f"TKT{random.randint(10000, 99999)}"
        
        # Save booking
        data_manager.add_user_booking(username, event_id, message, ticket_id)
        data_manager.save_events()
        
        print("\n✅ Payment successful!")
        print(f"Ticket ID: {ticket_id}")
        print(f"Seat: {message}")
        print("\n🎉 Booking confirmed!")
    else:
        # Payment failed - cancel booking
        event.seat_map.cancel_seat(row, seat)
        print("\n❌ Payment failed! Please try again.")
    
    pause()

def view_my_bookings(data_manager, username):
    """View user's bookings"""
    clear_screen()
    print_header("MY BOOKINGS")
    
    if username not in data_manager.user_bookings or not data_manager.user_bookings[username]:
        print("\n❌ No bookings found.")
        pause()
        return
    
    bookings = data_manager.user_bookings[username]
    
    for booking in bookings:
        event = data_manager.events.get(booking['event_id'])
        if event:
            print(f"\n{'─'*60}")
            print(f"Ticket ID: {booking['ticket_id']}")
            print(f"Event: {event.name}")
            print(f"Date: {event.date}")
            print(f"Seat: {booking['seat']}")
            print(f"Booked: {booking['time']}")
    
    print(f"\n{'─'*60}")
    pause()

# ==================== VENDOR MODULE ====================

def vendor_dashboard(data_manager, username):
    """Vendor dashboard"""
    while True:
        clear_screen()
        print_header(f"VENDOR DASHBOARD - {data_manager.users[username]['name']}")
        
        print("\n1. View Events with Stall Availability")
        print("2. Apply for Stall")
        print("3. My Applications")
        print("4. Logout")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            view_vendor_events(data_manager)
        elif choice == '2':
            apply_for_stall(data_manager, username)
        elif choice == '3':
            view_vendor_applications(data_manager, username)
        elif choice == '4':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def view_vendor_events(data_manager):
    """View events with vendor stall information"""
    clear_screen()
    print_header("EVENTS - STALL AVAILABILITY")
    
    if not data_manager.events:
        print("\n❌ No events available.")
        pause()
        return
    
    for event_id, event in data_manager.events.items():
        available = event.get_available_vendor_slots()
        
        print(f"\n{'─'*60}")
        print(f"Event ID: {event.event_id}")
        print(f"Name: {event.name}")
        print(f"Date: {event.date}")
        print(f"Location: {event.location}")
        print(f"Vendor Stalls: {available}/{event.total_vendor_slots} available")
    
    print(f"\n{'─'*60}")
    pause()

def apply_for_stall(data_manager, username):
    """Apply for a vendor stall"""
    clear_screen()
    print_header("APPLY FOR STALL")
    
    if not data_manager.events:
        print("\n❌ No events available.")
        pause()
        return
    
    # Show events
    for event_id, event in data_manager.events.items():
        available = event.get_available_vendor_slots()
        print(f"{event_id}. {event.name} - {available} stalls available")
    
    event_id = input("\nEnter Event ID: ").strip()
    
    if event_id not in data_manager.events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = data_manager.events[event_id]
    
    # Check if already applied
    if username in event.vendor_bookings:
        status = event.vendor_bookings[username]['status']
        print(f"\n❌ You have already applied for this event (Status: {status})")
        pause()
        return
    
    # Check availability
    if event.get_available_vendor_slots() == 0:
        print("\n❌ No stalls available!")
        pause()
        return
    
    print(f"\nEvent: {event.name}")
    print(f"Date: {event.date}")
    print(f"Location: {event.location}")
    
    business_name = input("\nBusiness Name: ").strip()
    business_type = input("Business Type: ").strip()
    description = input("Description: ").strip()
    
    confirm = input("\nSubmit application? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        event.vendor_bookings[username] = {
            'status': 'pending',
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'business_name': business_name,
            'business_type': business_type,
            'description': description
        }
        data_manager.save_events()
        
        print("\n✅ Application submitted! Wait for admin approval.")
    else:
        print("\n❌ Application cancelled.")
    
    pause()

def view_vendor_applications(data_manager, username):
    """View vendor's applications"""
    clear_screen()
    print_header("MY APPLICATIONS")
    
    applications = []
    
    for event_id, event in data_manager.events.items():
        if username in event.vendor_bookings:
            applications.append({
                'event': event,
                'application': event.vendor_bookings[username]
            })
    
    if not applications:
        print("\n❌ No applications found.")
        pause()
        return
    
    for app in applications:
        event = app['event']
        data = app['application']
        
        print(f"\n{'─'*60}")
        print(f"Event: {event.name}")
        print(f"Date: {event.date}")
        print(f"Business: {data['business_name']}")
        print(f"Status: {data['status'].upper()}")
        print(f"Applied: {data['time']}")
        
        if 'message' in data:
            print(f"Admin Message: {data['message']}")
    
    print(f"\n{'─'*60}")
    pause()

# ==================== ADMIN MODULE ====================

def admin_dashboard(data_manager, username):
    """Admin dashboard"""
    while True:
        clear_screen()
        print_header(f"ADMIN DASHBOARD - {data_manager.users[username]['name']}")
        
        print("\n1. Create Event")
        print("2. View All Events")
        print("3. Edit Event")
        print("4. Delete Event")
        print("5. View Bookings")
        print("6. Review Vendor Applications")
        print("7. Statistics")
        print("8. Logout")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            create_event(data_manager)
        elif choice == '2':
            view_all_events_admin(data_manager)
        elif choice == '3':
            edit_event(data_manager)
        elif choice == '4':
            delete_event(data_manager)
        elif choice == '5':
            view_all_bookings(data_manager)
        elif choice == '6':
            review_vendor_applications(data_manager)
        elif choice == '7':
            view_statistics(data_manager)
        elif choice == '8':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def create_event(data_manager):
    """Create a new event"""
    clear_screen()
    print_header("CREATE EVENT")
    
    event_id = input("Event ID: ").strip()
    
    if event_id in data_manager.events:
        print("\n❌ Event ID already exists!")
        pause()
        return
    
    name = input("Event Name: ").strip()
    date = input("Date (e.g., 2025-01-15): ").strip()
    location = input("Location: ").strip()
    price = float(input("Ticket Price: $").strip())
    
    rows = int(input("Number of seat rows: ").strip())
    seats_per_row = int(input("Seats per row: ").strip())
    vendor_slots = int(input("Number of vendor slots: ").strip())
    
    description = input("Event Description: ").strip()
    
    event = Event(event_id, name, date, location, price, rows, seats_per_row, vendor_slots)
    event.description = description
    
    data_manager.events[event_id] = event
    data_manager.save_events()
    
    print("\n✅ Event created successfully!")
    pause()

def view_all_events_admin(data_manager):
    """View all events (admin view)"""
    clear_screen()
    print_header("ALL EVENTS")
    
    if not data_manager.events:
        print("\n❌ No events created yet.")
        pause()
        return
    
    for event_id, event in data_manager.events.items():
        total_seats = event.seat_map.get_total_seats()
        booked_seats = total_seats - event.seat_map.get_available_count()
        
        print(f"\n{'─'*60}")
        print(f"ID: {event.event_id}")
        print(f"Name: {event.name}")
        print(f"Date: {event.date}")
        print(f"Location: {event.location}")
        print(f"Price: ${event.price}")
        print(f"Seats: {booked_seats}/{total_seats} booked")
        print(f"Vendors: {len([v for v in event.vendor_bookings.values() if v['status']=='approved'])}/{event.total_vendor_slots} approved")
    
    print(f"\n{'─'*60}")
    pause()

def edit_event(data_manager):
    """Edit an existing event"""
    clear_screen()
    print_header("EDIT EVENT")
    
    if not data_manager.events:
        print("\n❌ No events to edit.")
        pause()
        return
    
    for event_id in data_manager.events.keys():
        print(f"  {event_id}. {data_manager.events[event_id].name}")
    
    event_id = input("\nEnter Event ID to edit: ").strip()
    
    if event_id not in data_manager.events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = data_manager.events[event_id]
    
    print(f"\nEditing: {event.name}")
    print("\n1. Change Name")
    print("2. Change Date")
    print("3. Change Location")
    print("4. Change Price")
    print("5. Change Vendor Slots")
    print("6. Back")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        event.name = input("New Name: ").strip()
    elif choice == '2':
        event.date = input("New Date: ").strip()
    elif choice == '3':
        event.location = input("New Location: ").strip()
    elif choice == '4':
        event.price = float(input("New Price: $").strip())
    elif choice == '5':
        event.total_vendor_slots = int(input("New Vendor Slots: ").strip())
    elif choice == '6':
        return
    else:
        print("\n❌ Invalid choice!")
        pause()
        return
    
    data_manager.save_events()
    print("\n✅ Event updated successfully!")
    pause()

def delete_event(data_manager):
    """Delete an event"""
    clear_screen()
    print_header("DELETE EVENT")
    
    if not data_manager.events:
        print("\n❌ No events to delete.")
        pause()
        return
    
    for event_id in data_manager.events.keys():
        print(f"  {event_id}. {data_manager.events[event_id].name}")
    
    event_id = input("\nEnter Event ID to delete: ").strip()
    
    if event_id not in data_manager.events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = data_manager.events[event_id]
    
    confirm = input(f"\nDelete '{event.name}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        del data_manager.events[event_id]
        data_manager.save_events()
        print("\n✅ Event deleted successfully!")
    else:
        print("\n❌ Deletion cancelled.")
    
    pause()

def view_all_bookings(data_manager):
    """View all bookings across all events"""
    clear_screen()
    print_header("ALL BOOKINGS")
    
    total_bookings = 0
    
    for event_id, event in data_manager.events.items():
        bookings = event.seat_map.bookings
        
        if bookings:
            print(f"\n{'─'*60}")
            print(f"Event: {event.name}")
            print(f"{'─'*60}")
            
            for seat, info in bookings.items():
                print(f"Seat {seat} - User: {info['user']} - Time: {info['time']}")
                total_bookings += 1
    
    if total_bookings == 0:
        print("\n❌ No bookings yet.")
    else:
        print(f"\n{'─'*60}")
        print(f"Total Bookings: {total_bookings}")
    
    pause()

def review_vendor_applications(data_manager):
    """Review and approve/reject vendor applications"""
    clear_screen()
    print_header("VENDOR APPLICATIONS")
    
    pending_apps = []
    
    # Collect all pending applications
    for event_id, event in data_manager.events.items():
        for vendor_username, app in event.vendor_bookings.items():
            if app['status'] == 'pending':
                pending_apps.append({
                    'event_id': event_id,
                    'event': event,
                    'vendor': vendor_username,
                    'app': app
                })
    
    if not pending_apps:
        print("\n❌ No pending applications.")
        pause()
        return
    
    # Display applications
    for idx, item in enumerate(pending_apps, 1):
        print(f"\n{'─'*60}")
        print(f"Application #{idx}")
        print(f"Event: {item['event'].name}")
        print(f"Vendor: {item['vendor']}")
        print(f"Business: {item['app']['business_name']}")
        print(f"Type: {item['app']['business_type']}")
        print(f"Description: {item['app']['description']}")
        print(f"Applied: {item['app']['time']}")
    
    print(f"\n{'─'*60}")
    
    app_num = input("\nSelect application # to review (0 to cancel): ").strip()
    
    try:
        app_num = int(app_num)
        if app_num == 0:
            return
        if 1 <= app_num <= len(pending_apps):
            selected = pending_apps[app_num - 1]
            
            print("\n1. Approve")
            print("2. Reject")
            
            decision = input("\nChoice: ").strip()
            
            if decision == '1':
                selected['app']['status'] = 'approved'
                message = input("Message to vendor (optional): ").strip()
                if message:
                    selected['app']['message'] = message
                print("\n✅ Application approved!")
            elif decision == '2':
                selected['app']['status'] = 'rejected'
                message = input("Rejection reason: ").strip()
                selected['app']['message'] = message
                print("\n✅ Application rejected!")
            else:
                print("\n❌ Invalid choice!")
                pause()
                return
            
            data_manager.save_events()
            pause()
        else:
            print("\n❌ Invalid application number!")
            pause()
    except ValueError:
        print("\n❌ Invalid input!")
        pause()

def view_statistics(data_manager):
    """View platform statistics"""
    clear_screen()
    print_header("PLATFORM STATISTICS")
    
    total_events = len(data_manager.events)
    total_users = len([u for u in data_manager.users.values() if u['role'] == 'user'])
    total_vendors = len([u for u in data_manager.users.values() if u['role'] == 'vendor'])
    
    total_bookings = 0
    total_revenue = 0
    
    for event in data_manager.events.values():
        bookings_count = len(event.seat_map.bookings)
        total_bookings += bookings_count
        total_revenue += bookings_count * event.price
    
    print(f"\nTotal Events: {total_events}")
    print(f"Total Users: {total_users}")
    print(f"Total Vendors: {total_vendors}")
    print(f"Total Bookings: {total_bookings}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    
    print(f"\n{'─'*60}")
    print("EVENT-WISE BREAKDOWN")
    print(f"{'─'*60}")
    
    for event in data_manager.events.values():
        bookings_count = len(event.seat_map.bookings)
        revenue = bookings_count * event.price
        total_seats = event.seat_map.get_total_seats()
        occupancy = (bookings_count / total_seats * 100) if total_seats > 0 else 0
        
        print(f"\n{event.name}")
        print(f"  Bookings: {bookings_count}/{total_seats} ({occupancy:.1f}%)")
        print(f"  Revenue: ${revenue:.2f}")
    
    pause()

# ==================== MAIN PROGRAM ====================

def main():
    """Main program entry point"""
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Welcome screen
    clear_screen()
    print_header("WELCOME TO FESTIO")
    print("\n🎉 Your Complete Event Management Platform 🎉")
    print("\nBook tickets, manage events, and connect with vendors!")
    print("\nFeatures:")
    print("  ✓ Browse and book event tickets")
    print("  ✓ Interactive seat selection")
    print("  ✓ Vendor stall booking")
    print("  ✓ Complete event management")
    pause()
    
    # Start in guest mode
    current_user = None
    current_role = None
    
    while True:
        if not current_user:
            # Guest mode
            current_user, current_role = guest_mode(data_manager)
            
            if not current_user:
                # User chose to exit
                break
        
        # Role-based dashboard
        if current_role == 'user':
            user_dashboard(data_manager, current_user)
            current_user = None
        
        elif current_role == 'vendor':
            vendor_dashboard(data_manager, current_user)
            current_user = None
        
        elif current_role == 'admin':
            admin_dashboard(data_manager, current_user)
            current_user = None
    
    print("\n" + "="*60)
    print("Thank you for using FESTIO!".center(60))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()