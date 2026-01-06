import os
import json
from datetime import datetime
import random

# ============ FILE PATHS ====================
USERS_FILE = "users.json"
EVENTS_FILE = "events.json"
BOOKINGS_FILE = "user_bookings.json"

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

# ======= FILE OPERATIONS ====================

def initialize_files():
    """Create JSON files if they don't exist"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            'admin': {
                'password': 'admin123',
                'role': 'admin',
                'name': 'Administrator'
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
    
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'w') as f:
            json.dump({}, f, indent=2)
    
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump({}, f, indent=2)

def load_users():
    """Load users from file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save users to file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_events():
    """Load events from file"""
    try:
        with open(EVENTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_events(events):
    """Save events to file"""
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=2)

def load_bookings():
    """Load user bookings from file"""
    try:
        with open(BOOKINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_bookings(bookings):
    """Save user bookings to file"""
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=2)

# ============= SEAT MAP FUNCTIONS ===============

def create_seat_map(rows, seats_per_row):
    """Create a new seat map 
    this is a nested list constructor 
        _ is a variable but shows that im not gonna use it """ 
    seatm = [[True for _ in range(seats_per_row)]
                for _ in range(rows)
                ]
    
    return seatm

def book_seat(event, row, seat, username):
    """Book a seat for a user"""
    rows = event['rows']
    seats_per_row = event['seats_per_row']
    seat_map = event['seats']
    
    if ((0 <= row and row < rows) and (0 <= seat and seat < seats_per_row)):
        if seat_map[row][seat]:
            seat_map[row][seat] = False
            seat_label = f"{row+1}{chr(65+seat)}"
            event['bookings'][seat_label] = {
                "user": username,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True, seat_label
        else:
            return False, "Seat already occupied"
    return False, "Invalid seat"

def cancel_seat(event, row, seat):
    """Cancel a seat booking"""
    rows = event['rows']
    seats_per_row = event['seats_per_row']
    seat_map = event['seats']
    
    if 0 <= row and row < rows and 0 <= seat and seat < seats_per_row:
        if not seat_map[row][seat]:
            seat_map[row][seat] = True
            seat_label = f"{row+1}{chr(65+seat)}"
            if seat_label in event['bookings']:
                del event['bookings'][seat_label]
            return True
    return False

def display_seat_map(event):
    """Display the seat map"""
    print("\n[X] = Occupied  [ ] = Available\n")
    
    seat_map = event['seats']
    seats_per_row = event['seats_per_row']
    
    # Column headers
    print("   ", end="")
    for i in range(seats_per_row):
        print(f"  {chr(65+i)} ", end="")
    print("\n")
    
    # Rows with seats
    for row_idx, row in enumerate(seat_map):
        print(f"{row_idx+1:2d} ", end="")
        for seat_idx, is_available in enumerate(row):
            if is_available:
                print("[ ]", end=" ")
            else:
                print("[X]", end=" ")
        print()
    print()

def get_available_seats(event):
    """Get number of available seats"""
    count = 0
    for row in event['seats']:
        count += sum(row)
    return count

def get_total_seats(event):
    """Get total number of seats"""
    return event['rows'] * event['seats_per_row']

# =============== EVENT FUNCTIONS =================

def create_event(event_id, name, date, location, price, rows, seats_per_row, vendor_slots, description=""):
    """Create a new event"""
    event = {
        'event_id': event_id,
        'name': name,
        'date': date,
        'location': location,
        'price': price,
        'rows': rows,
        'seats_per_row': seats_per_row,
        'seats': create_seat_map(rows, seats_per_row),
        'bookings': {},
        'total_vendor_slots': vendor_slots,
        'vendor_bookings': {},
        'description': description
    }
    return event 

def get_available_vendor_slots(event):
    """Get number of available vendor slots"""
    inuse = 0 
    for v in event['vendor_bookings'].values():
        if v['status'] == 'approved':
            inuse +=1 
    approved = inuse 
    return event['total_vendor_slots'] - approved

# ================= BOOKING FUNCTIONS ==========================

def add_user_booking(bookings, username, event_id, seat_label, ticket_id):
    """Add a booking for a user"""
    if username not in bookings:
        bookings[username] = []
    
    bookings[username].append({
        'ticket_id': ticket_id,
        'event_id': event_id,
        'seat': seat_label,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ========= AUTHENTICATION ===================

def login():
    """Handle user login"""
    print_header("LOGIN")
    
    users = load_users()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    if username in users: # checks if the username exists in users or not 
        if users[username]['password'] == password: # checks if the password is correct or not 
            print(f"\n✅ Login successful! Welcome, {users[username]['name']}")
            pause()
            return username, users[username]['role']
        else:
            print("\n❌ Incorrect password!")
            pause()
            return None, None
    else:
        print("\n❌ User not found!")
        pause()
        return None, None

def register():
    """Handle user registration"""
    print_header("REGISTER")
    
    users = load_users()
    
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
    
    if username in users:
        print("\n❌ Username already exists!")
        pause()
        return
    
    password = input("Password: ").strip()
    name = input("Full Name: ").strip()
    
    users[username] = {
        'password': password,
        'role': role,
        'name': name
    }
    save_users(users)
    
    print(f"\n✅ Registration successful! You can now login as {role}.")
    pause()

# ========== GUEST MODULE ================

def browse_events(is_guest=False):
    """Display all events"""
    clear_screen()
    print_header("AVAILABLE EVENTS")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events available at the moment.")
        pause()
        return
    
    for event_id, event in events.items():
        available_seats = get_available_seats(event)
        total_seats = get_total_seats(event)
        
        print(f"\n{'─'*60}")
        print(f"Event ID: {event['event_id']}")
        print(f"Name: {event['name']}")
        print(f"Date: {event['date']}")
        print(f"Location: {event['location']}")
        print(f"Price: {event['price']}")
        print(f"Seats Available: {available_seats}/{total_seats}")
        print(f"Vendor Slots Available: {get_available_vendor_slots(event)}/{event['total_vendor_slots']}")
    
    print(f"\n{'─'*60}")
    
    if is_guest:
        print("\n💡 Login to book tickets!")
    
    pause()

def view_event_details(is_guest=False):
    """View details of a specific event"""
    clear_screen()
    print_header("EVENT DETAILS")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events available.")
        pause()
        return None
    
    # Show all event list
    for event_id in events.keys():
        print(f"  {event_id}. {events[event_id]['name']}") # Prints event id and its name 
    
    event_id = input("\nEnter Event ID: ").strip()
    
    if event_id not in events: # checks if the entered id is in events or not 
        print("\n❌ Event not found!")
        pause()
        return None
    
    event = events[event_id] # gets a;; the info of the event 
    
    clear_screen()
    print_header(f"EVENT: {event['name']}")
    print(f"\nDate: {event['date']}")
    print(f"Location: {event['location']}")
    print(f"Price: {event['price']}")
    print(f"Description: {event['description'] if event['description'] else 'No description'}")
    print(f"\n{'─'*60}")
    print(f"Total Seats: {get_total_seats(event)}")
    print(f"Available Seats: {get_available_seats(event)}")
    print(f"Vendor Slots: {get_available_vendor_slots(event)}/{event['total_vendor_slots']} available")
    
    if is_guest:
        print("\n💡 Login to book tickets!")
        pause()
        return None
    
    return event_id

def guest_mode():
    # Guest browsing mode
    while True: # keeps the guest menu running continuously until the user chooses to login, register successfully, or exit.
        clear_screen()
        print_header("GUEST MODE - CARNIVAL CORNER EVENT PLATFORM")
        
        print("\n1. Browse Events")
        print("2. View Event Details")
        print("3. Login")
        print("4. Register")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            browse_events(is_guest=True)
        elif choice == '2':
            view_event_details(is_guest=True)
        elif choice == '3':
            username, role = login()
            if username:
                return username, role
        elif choice == '4':
            register()
        elif choice == '5':
            print("\n👋 Thank you for visiting Carnival Corner!")
            return None, None
        else:
            print("\n❌ Invalid choice!")
            pause()

# ============ USER MODULE ====================

def user_dashboard(username):
    """User dashboard"""
    users = load_users()
    
    while True: # make it run in a loop until user enters a trigger 
        clear_screen()
        print_header(f"USER DASHBOARD - {users[username]['name']}") # prints the name of the user from user.json
        # print_header is defined by us to print the whole style of the header 
        print("\n1. Browse Events")
        print("2. Book Ticket")
        print("3. My Bookings")
        print("4. Logout")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            browse_events()
        elif choice == '2':
            book_ticket(username)
        elif choice == '3':
            view_my_bookings(username)
        elif choice == '4':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def book_ticket(username):
    """Book a ticket for an event"""
    event_id = view_event_details()
    
    if not event_id:
        return None 
    
    events = load_events()
    event = events[event_id]
    
    if get_available_seats(event) == 0:
        print("\n❌ Sorry, event is fully booked!")
        pause()
        return None 
    
    print("\n" + "─"*60)
    print("SEAT MAP")
    print("─"*60)
    display_seat_map(event)
    
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
    seat = ord(seat_letter) - 65 # ord converts the letter to its ASCI or unicode 
    
    # Book the seat
    success, message = book_seat(event, row, seat, username)
    
    if not success:
        print(f"\n❌ {message}")
        pause()
        return
    
    # Payment simulation
    print("\n" + "─"*60)
    print("PAYMENT")
    print("─"*60)
    print(f"Event: {event['name']}")
    print(f"Seat: {message}")
    print(f"Price: {event['price']}")
    
    confirm = input("\nProceed to payment? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        # Cancel the booking
        cancel_seat(event, row, seat)
        save_events(events)
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
        bookings = load_bookings()
        add_user_booking(bookings, username, event_id, message, ticket_id)
        save_bookings(bookings)
        save_events(events)
        
        print("\n✅ Payment successful!")
        print(f"Ticket ID: {ticket_id}")
        print(f"Seat: {message}")
        print("\n🎉 Booking confirmed!")
    else:
        # Payment failed - cancel booking
        cancel_seat(event, row, seat)
        save_events(events)
        print("\n❌ Payment failed! Please try again.")
    
    pause()

def view_my_bookings(username):
    """View user's bookings"""
    clear_screen()
    print_header("MY BOOKINGS")
    
    bookings = load_bookings()
    events = load_events()
    
    if username not in bookings or not bookings[username]:
        print("\n❌ No bookings found.")
        pause()
        return
    
    user_bookings = bookings[username]
    
    for booking in user_bookings:
        event = events.get(booking['event_id'])
        if event:
            print(f"\n{'─'*60}")
            print(f"Ticket ID: {booking['ticket_id']}")
            print(f"Event: {event['name']}")
            print(f"Date: {event['date']}")
            print(f"Seat: {booking['seat']}")
            print(f"Booked: {booking['time']}")
    
    print(f"\n{'─'*60}")
    pause()

# =============== VENDOR MODULE ====================

def vendor_dashboard(username):
    """Vendor dashboard"""
    users = load_users()
    
    while True:
        clear_screen()
        print_header(f"VENDOR DASHBOARD - {users[username]['name']}")
        
        print("\n1. View Events with Stall Availability")
        print("2. Apply for Stall")
        print("3. My Applications")
        print("4. Logout")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            view_vendor_events()
        elif choice == '2':
            apply_for_stall(username)
        elif choice == '3':
            view_vendor_applications(username)
        elif choice == '4':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def view_vendor_events():
    """View events with vendor stall information"""
    clear_screen()
    print_header("EVENTS - STALL AVAILABILITY")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events available.")
        pause()
        return
    
    for event_id, event in events.items():
        available = get_available_vendor_slots(event)
        
        print(f"\n{'─'*60}")
        print(f"Event ID: {event['event_id']}")
        print(f"Name: {event['name']}")
        print(f"Date: {event['date']}")
        print(f"Location: {event['location']}")
        print(f"Vendor Stalls: {available}/{event['total_vendor_slots']} available")
    
    print(f"\n{'─'*60}")
    pause()

def apply_for_stall(username):
    """Apply for a vendor stall"""
    clear_screen()
    print_header("APPLY FOR STALL")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events available.")
        pause()
        return
    
    # Show events
    for event_id, event in events.items():
        available = get_available_vendor_slots(event)
        print(f"{event_id}. {event['name']} - {available} stalls available")
    
    event_id = input("\nEnter Event ID: ").strip()
    
    if event_id not in events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = events[event_id]
    
    # Check if already applied
    if username in event['vendor_bookings']:
        status = event['vendor_bookings'][username]['status']
        print(f"\n❌ You have already applied for this event (Status: {status})")
        pause()
        return
    
    # Check availability
    if get_available_vendor_slots(event) == 0:
        print("\n❌ No stalls available!")
        pause()
        return
    
    print(f"\nEvent: {event['name']}")
    print(f"Date: {event['date']}")
    print(f"Location: {event['location']}")
    
    business_name = input("\nBusiness Name: ").strip()
    business_type = input("Business Type: ").strip()
    description = input("Description: ").strip()
    
    confirm = input("\nSubmit application? (yes/no): ").strip().lower()
    
    if confirm == 'yes' or 'y':
        event['vendor_bookings'][username] = {
            'status': 'pending',
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'business_name': business_name,
            'business_type': business_type,
            'description': description
        }
        save_events(events)
        
        print("\n✅ Application submitted! Wait for admin approval.")
    else:
        print("\n❌ Application cancelled.")
    
    pause()

def view_vendor_applications(username):
    """View vendor's applications"""
    clear_screen()
    print_header("MY APPLICATIONS")
    
    events = load_events()
    applications = []
    
    for event_id, event in events.items():
        if username in event['vendor_bookings']:
            applications.append({
                'event': event,
                'application': event['vendor_bookings'][username]
            })
    
    if not applications:
        print("\n❌ No applications found.")
        pause()
        return
    
    for app in applications:
        event = app['event']
        data = app['application']
        
        print(f"\n{'─'*60}")
        print(f"Event: {event['name']}")
        print(f"Date: {event['date']}")
        print(f"Business: {data['business_name']}")
        print(f"Status: {data['status'].upper()}")
        print(f"Applied: {data['time']}")
        
        if 'message' in data:
            print(f"Admin Message: {data['message']}")
    
    print(f"\n{'─'*60}")
    pause()

# ================ ADMIN MODULE ====================

def admin_dashboard(username):
    """Admin dashboard"""
    users = load_users()
    
    while True:
        clear_screen()
        print_header(f"ADMIN DASHBOARD - {users[username]['name']}")
        
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
            create_event_admin()
        elif choice == '2':
            view_all_events_admin()
        elif choice == '3':
            edit_event()
        elif choice == '4':
            delete_event()
        elif choice == '5':
            view_all_bookings()
        elif choice == '6':
            review_vendor_applications()
        elif choice == '7':
            view_statistics()
        elif choice == '8':
            print("\n👋 Logged out successfully!")
            pause()
            break
        else:
            print("\n❌ Invalid choice!")
            pause()

def create_event_admin():
    """Create a new event"""
    clear_screen()
    print_header("CREATE EVENT")
    
    events = load_events()
    
    event_id = input("Event ID: ").strip()
    
    if event_id in events:
        print("\n❌ Event ID already exists!")
        pause()
        return
    
    name = input("Event Name: ").strip()
    date = input("Date (e.g., 2025-01-15): ").strip()
    location = input("Location: ").strip()
    price = float(input("Ticket Price: ").strip())
    
    rows = int(input("Number of seat rows: ").strip())
    seats_per_row = int(input("Seats per row: ").strip())
    vendor_slots = int(input("Number of vendor slots: ").strip())
    
    description = input("Event Description: ").strip()
    
    event = create_event(event_id, name, date, location, price, rows, seats_per_row, vendor_slots, description)
    
    events[event_id] = event
    save_events(events)
    
    print("\n✅ Event created successfully!")
    pause()

def view_all_events_admin():
    """View all events (admin view)"""
    clear_screen()
    print_header("ALL EVENTS")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events created yet.")
        pause()
        return
    
    for event_id, event in events.items():
        total_seats = get_total_seats(event)
        booked_seats = total_seats - get_available_seats(event)
        
        print(f"\n{'─'*60}")
        print(f"ID: {event['event_id']}")
        print(f"Name: {event['name']}")
        print(f"Date: {event['date']}")
        print(f"Location: {event['location']}")
        print(f"Price: {event['price']}")
        print(f"Seats: {booked_seats}/{total_seats} booked")
        print(f"Vendors: {len([v for v in event['vendor_bookings'].values() if v['status']=='approved'])}/{event['total_vendor_slots']} approved")
    
    print(f"\n{'─'*60}")
    pause()

def edit_event():
    """Edit an existing event"""
    clear_screen()
    print_header("EDIT EVENT")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events to edit.")
        pause()
        return
    
    for event_id in events.keys():
        print(f"  {event_id}. {events[event_id]['name']}")
    
    event_id = input("\nEnter Event ID to edit: ").strip()
    
    if event_id not in events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = events[event_id]
    
    print(f"\nEditing: {event['name']}")
    print("\n1. Change Name")
    print("2. Change Date")
    print("3. Change Location")
    print("4. Change Price")
    print("5. Change Vendor Slots")
    print("6. Back")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        event['name'] = input("New Name: ").strip()
    elif choice == '2':
        event['date'] = input("New Date: ").strip()
    elif choice == '3':
        event['location'] = input("New Location: ").strip()
    elif choice == '4':
        event['price'] = float(input("New Price: ").strip())
    elif choice == '5':
        event['total_vendor_slots'] = int(input("New Vendor Slots: ").strip())
    elif choice == '6':
        return
    else:
        print("\n❌ Invalid choice!")
        pause()
        return
    
    save_events(events)
    print("\n✅ Event updated successfully!")
    pause()

def delete_event():
    """Delete an event"""
    clear_screen()
    print_header("DELETE EVENT")
    
    events = load_events()
    
    if not events:
        print("\n❌ No events to delete alr.")
        pause()
        return
    
    for event_id in events.keys():
        print(f"  {event_id}. {events[event_id]['name']}")
    
    event_id = input("\nEnter Event ID to delete: ").strip()
    
    if event_id not in events:
        print("\n❌ Event not found!")
        pause()
        return
    
    event = events[event_id]
    
    confirm = input(f"\nDelete '{event['name']}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes' or 'y':
        del events[event_id]
        save_events(events)
        print("\n✅ Event deleted successfully!")
    else:
        print("\n❌ Deletion cancelled.")
    
    pause()

def view_all_bookings():
    """View all bookings across all events"""
    clear_screen()
    print_header("ALL BOOKINGS")
    
    events = load_events()
    total_bookings = 0
    
    for event_id, event in events.items():
        bookings = event['bookings']
        
        if bookings:
            print(f"\n{'─'*60}")
            print(f"Event: {event['name']}")
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

def review_vendor_applications():
    """Review and approve/reject vendor applications"""
    clear_screen()
    print_header("VENDOR APPLICATIONS")
    
    events = load_events()
    pending_apps = []
    
    # Collect all pending applications
    for event_id, event in events.items():
        for vendor_username, app in event['vendor_bookings'].items():
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
        print(f"Event: {item['event']['name']}")
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
        if 1 <= app_num and app_num <= len(pending_apps):
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
            
            save_events(events)
            pause()
        else:
            print("\n❌ Invalid application number!")
            pause()
    except ValueError:
        print("\n❌ Invalid input!")
        pause()

def view_statistics():
    """View platform statistics"""
    clear_screen()
    print_header("PLATFORM STATISTICS")
    
    users = load_users()
    events = load_events()
    
    total_events = len(events)
    total_users = len([u for u in users.values() if u['role'] == 'user'])
    total_vendors = len([v for v in users.values() if v['role'] == 'vendor'])
    
    total_bookings = 0
    total_revenue = 0
    
    for event in events.values():
        bookings_count = len(event['bookings'])
        total_bookings += bookings_count
        total_revenue += bookings_count * event['price']
    
    print(f"\nTotal Events: {total_events}")
    print(f"Total Users: {total_users}")
    print(f"Total Vendors: {total_vendors}")
    print(f"Total Bookings: {total_bookings}")
    print(f"Total Revenue: {total_revenue:.2f}")
    
    print(f"\n{'─'*60}")
    print("EVENT-WISE BREAKDOWN")
    print(f"{'─'*60}")
    
    for event in events.values():
        bookings_count = len(event['bookings'])
        revenue = bookings_count * event['price']
        total_seats = get_total_seats(event)
        if total_seats > 0:
            occupancy = (bookings_count / total_seats * 100)
        else: 
            occupancy = 0
        
        print(f"\n{event['name']}")
        print(f"  Bookings: {bookings_count}/{total_seats} ({occupancy:.1f}%)")
        print(f"  Revenue: {revenue:.2f}")
    
    pause()

# ================= MAIN PROGRAM ====================

def main():
    """Main program entry point"""
    
    # Initialize files
    initialize_files()
    
    # Welcome screen
    clear_screen()
    print_header("WELCOME TO CARNIVAL CORNER")
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
            current_user, current_role = guest_mode()
            
            if not current_user:
                # User chose to exit
                break
        
        # Role-based selection
        if current_role == 'user':
            user_dashboard(current_user)
            current_user = None
        
        elif current_role == 'vendor':
            vendor_dashboard(current_user)
            current_user = None
        
        elif current_role == 'admin':
            admin_dashboard(current_user)
            current_user = None
    
    print("\n" + "="*60)
    print("Thank you for using Carnival Corner!".center(60))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()