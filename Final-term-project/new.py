import os
import json
from datetime import datetime


class SeatMap:
    def __init__(self, rows, seats_per_row):
        self.rows = rows
        self.seats_per_row = seats_per_row
        # Create seat map with all seats available (True = available, False = occupied)
        self.seats = [[True for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}  # Track who booked which seat
    
    def book_seat(self, row, seat, passenger_name=""):
        """Book a seat (mark as occupied)"""
        if 0 <= row < self.rows and 0 <= seat < self.seats_per_row:
            if self.seats[row][seat]:
                self.seats[row][seat] = False
                seat_label = f"{row+1}{chr(65+seat)}"
                self.bookings[seat_label] = {
                    "passenger": passenger_name,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return True, seat_label
            else:
                return False, f"Seat {row+1}{chr(65+seat)} is already occupied!"
        else:
            return False, "Invalid seat position!"
    
    def cancel_seat(self, row, seat):
        """Cancel a seat booking (mark as available)"""
        if 0 <= row < self.rows and 0 <= seat < self.seats_per_row:
            if not self.seats[row][seat]:
                self.seats[row][seat] = True
                seat_label = f"{row+1}{chr(65+seat)}"
                if seat_label in self.bookings:
                    del self.bookings[seat_label]
                return True, f"Seat {seat_label} has been cancelled successfully!"
            else:
                return False, f"Seat {row+1}{chr(65+seat)} is not booked!"
        else:
            return False, "Invalid seat position!"
    
    def get_available_seats(self):
        """Return list of available seats"""
        available = []
        for row_idx, row in enumerate(self.seats):
            for seat_idx, is_available in enumerate(row):
                if is_available:
                    available.append(f"{row_idx+1}{chr(65+seat_idx)}")
        return available
    
    def get_occupied_seats(self):
        """Return list of occupied seats"""
        occupied = []
        for row_idx, row in enumerate(self.seats):
            for seat_idx, is_available in enumerate(row):
                if not is_available:
                    occupied.append(f"{row_idx+1}{chr(65+seat_idx)}")
        return occupied
    
    def get_booking_info(self, row, seat):
        """Get booking information for a specific seat"""
        seat_label = f"{row+1}{chr(65+seat)}"
        return self.bookings.get(seat_label, None)
    
    def display(self, show_legend=True):
        """Display the seat map"""
        print("\n" + "="*50)
        print("SEAT MAP".center(50))
        print("="*50)
        if show_legend:
            print("[X] = Occupied  [ ] = Available")
            print("="*50)
        print()
        
        # Display column headers (A, B, C, D, etc.)
        print("   ", end="")
        for i in range(self.seats_per_row):
            print(f"  {chr(65+i)} ", end="")
        print("\n")
        
        # Display rows with seat status
        for row_idx, row in enumerate(self.seats):
            print(f"{row_idx+1:2d} ", end="")
            for seat_idx, is_available in enumerate(row):
                # Add aisle space in the middle for airplane-style layout
                if seat_idx == self.seats_per_row // 2:
                    print("  ", end="")
                
                if is_available:
                    print("[ ]", end=" ")
                else:
                    print("[X]", end=" ")
            print()
        
        print("\n" + "="*50 + "\n")
    
    def get_statistics(self):
        """Get booking statistics"""
        total_seats = self.rows * self.seats_per_row
        occupied = len(self.get_occupied_seats())
        available = total_seats - occupied
        occupancy_rate = (occupied / total_seats) * 100
        
        return {
            "total": total_seats,
            "occupied": occupied,
            "available": available,
            "occupancy_rate": occupancy_rate
        }
    
    def save_to_file(self, filename="seat_bookings.json"):
        """Save current bookings to a file"""
        data = {
            "rows": self.rows,
            "seats_per_row": self.seats_per_row,
            "seats": self.seats,
            "bookings": self.bookings
        }
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Bookings saved to {filename}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def load_from_file(self, filename="seat_bookings.json"):
        """Load bookings from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.rows = data["rows"]
            self.seats_per_row = data["seats_per_row"]
            self.seats = data["seats"]
            self.bookings = data["bookings"]
            return True, f"Bookings loaded from {filename}"
        except FileNotFoundError:
            return False, "No saved bookings found"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"


class StallMap:
    def __init__(self, rows, stalls_per_row):
        self.rows = rows
        self.stalls_per_row = stalls_per_row
        # Create stall map with all stalls available (True = available, False = occupied)
        self.stalls = [[True for _ in range(stalls_per_row)] for _ in range(rows)]
        self.bookings = {}  # Track who booked which stall
    
    def book_stall(self, row, stall, vendor_name=""):
        """Book a stall (mark as occupied)"""
        if 0 <= row < self.rows and 0 <= stall < self.stalls_per_row:
            if self.stalls[row][stall]:
                self.stalls[row][stall] = False
                stall_label = f"{row+1}{chr(65+stall)}"
                self.bookings[stall_label] = {
                    "vendor": vendor_name,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return True, stall_label
            else:
                return False, f"Stall {row+1}{chr(65+stall)} is already occupied!"
        else:
            return False, "Invalid stall position!"
    
    def cancel_stall(self, row, stall):
        """Cancel a stall booking (mark as available)"""
        if 0 <= row < self.rows and 0 <= stall < self.stalls_per_row:
            if not self.stalls[row][stall]:
                self.stalls[row][stall] = True
                stall_label = f"{row+1}{chr(65+stall)}"
                if stall_label in self.bookings:
                    del self.bookings[stall_label]
                return True, f"Stall {stall_label} has been cancelled successfully!"
            else:
                return False, f"Stall {row+1}{chr(65+stall)} is not booked!"
        else:
            return False, "Invalid stall position!"
    
    def get_available_stalls(self):
        """Return list of available stalls"""
        available = []
        for row_idx, row in enumerate(self.stalls):
            for stall_idx, is_available in enumerate(row):
                if is_available:
                    available.append(f"{row_idx+1}{chr(65+stall_idx)}")
        return available
    
    def get_occupied_stalls(self):
        """Return list of occupied stalls"""
        occupied = []
        for row_idx, row in enumerate(self.stalls):
            for stall_idx, is_available in enumerate(row):
                if not is_available:
                    occupied.append(f"{row_idx+1}{chr(65+stall_idx)}")
        return occupied
    
    def get_booking_info(self, row, stall):
        """Get booking information for a specific stall"""
        stall_label = f"{row+1}{chr(65+stall)}"
        return self.bookings.get(stall_label, None)
    
    def display(self, show_legend=True):
        """Display the stall map"""
        print("\n" + "="*50)
        print("STALL MAP".center(50))
        print("="*50)
        if show_legend:
            print("[X] = Occupied  [ ] = Available")
            print("="*50)
        print()
        
        # Display column headers (A, B, C, D, etc.)
        print("   ", end="")
        for i in range(self.stalls_per_row):
            print(f"  {chr(65+i)} ", end="")
        print("\n")
        
        # Display rows with stall status
        for row_idx, row in enumerate(self.stalls):
            print(f"{row_idx+1:2d} ", end="")
            for stall_idx, is_available in enumerate(row):
                if is_available:
                    print("[ ]", end=" ")
                else:
                    print("[X]", end=" ")
            print()
        
        print("\n" + "="*50 + "\n")
    
    def get_statistics(self):
        """Get booking statistics"""
        total_stalls = self.rows * self.stalls_per_row
        occupied = len(self.get_occupied_stalls())
        available = total_stalls - occupied
        occupancy_rate = (occupied / total_stalls) * 100
        
        return {
            "total": total_stalls,
            "occupied": occupied,
            "available": available,
            "occupancy_rate": occupancy_rate
        }
    
    def save_to_file(self, filename="stall_bookings.json"):
        """Save current bookings to a file"""
        data = {
            "rows": self.rows,
            "stalls_per_row": self.stalls_per_row,
            "stalls": self.stalls,
            "bookings": self.bookings
        }
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Bookings saved to {filename}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def load_from_file(self, filename="stall_bookings.json"):
        """Load bookings from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.rows = data["rows"]
            self.stalls_per_row = data["stalls_per_row"]
            self.stalls = data["stalls"]
            self.bookings = data["bookings"]
            return True, f"Bookings loaded from {filename}"
        except FileNotFoundError:
            return False, "No saved bookings found"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def parse_seat_input(seat_input):
    """Parse seat input like '5B' into row and seat indices"""
    seat_input = seat_input.strip().upper()
    
    # Extract row number and seat letter
    row_str = ""
    seat_letter = ""
    
    for char in seat_input:
        if char.isdigit():
            row_str += char
        elif char.isalpha():
            seat_letter += char
    
    if not row_str or not seat_letter or len(seat_letter) != 1:
        return None, None
    
    try:
        row = int(row_str) - 1  # Convert to 0-indexed
        seat = ord(seat_letter) - 65  # Convert A->0, B->1, etc.
        return row, seat
    except:
        return None, None


def display_menu():
    # Display the main menu
    print("\n" + "="*50)
    print("SEAT & STALL BOOKING SYSTEM".center(50))
    print("="*50)
    print("SEAT OPTIONS:")
    print("1. View Seat Map")
    print("2. Book a Seat")
    print("3. Cancel a Booking")
    print("4. View Available Seats")
    print("5. View My Bookings")
    print("6. View Statistics")
    print("7. Save Bookings")
    print("8. Load Bookings")
    print()
    print("VENDOR STALL OPTIONS:")
    print("9. View Stall Map")
    print("10. Book a Stall")
    print("11. Cancel a Stall Booking")
    print("12. View Available Stalls")
    print("13. View Vendor Bookings")
    print("14. View Stall Statistics")
    print("15. Save Stall Bookings")
    print("16. Load Stall Bookings")
    print()
    print("17. Exit")
    print("="*50)


def book_seat_interactive(seat_map):
    """Interactive seat booking"""
    seat_map.display()
    
    available = seat_map.get_available_seats()
    if not available:
        print("❌ Sorry, all seats are fully booked!")
        input("\nPress Enter to continue...")
        return
    
    print(f"Available seats: {len(available)}")
    print("Enter seat in format: Row+Letter (e.g., 5B, 10A)")
    
    seat_input = input("\nEnter seat to book (or 'back' to return): ").strip()
    
    if seat_input.lower() == 'back':
        return
    
    row, seat = parse_seat_input(seat_input)
    
    if row is None or seat is None:
        print("❌ Invalid seat format! Use format like '5B' or '10A'")
        input("\nPress Enter to continue...")
        return
    
    passenger_name = input("Enter passenger name: ").strip()
    
    success, message = seat_map.book_seat(row, seat, passenger_name)
    
    if success:
        print(f"\n✅ Success! Seat {message} booked for {passenger_name}")
    else:
        print(f"\n❌ {message}")
    
    input("\nPress Enter to continue...")


def cancel_seat_interactive(seat_map):
    """Interactive seat cancellation"""
    seat_map.display()
    
    occupied = seat_map.get_occupied_seats()
    if not occupied:
        print("❌ No seats are currently booked!")
        input("\nPress Enter to continue...")
        return
    
    print(f"Occupied seats: {', '.join(occupied)}")
    print("Enter seat in format: Row+Letter (e.g., 5B, 10A)")
    
    seat_input = input("\nEnter seat to cancel (or 'back' to return): ").strip()
    
    if seat_input.lower() == 'back':
        return
    
    row, seat = parse_seat_input(seat_input)
    
    if row is None or seat is None:
        print("❌ Invalid seat format! Use format like '5B' or '10A'")
        input("\nPress Enter to continue...")
        return
    
    # Show booking info before cancelling
    booking_info = seat_map.get_booking_info(row, seat)
    if booking_info:
        print(f"\nBooking Details:")
        print(f"  Passenger: {booking_info['passenger']}")
        print(f"  Booked at: {booking_info['time']}")
        confirm = input("\nConfirm cancellation? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancellation aborted.")
            input("\nPress Enter to continue...")
            return
    
    success, message = seat_map.cancel_seat(row, seat)
    
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")
    
    input("\nPress Enter to continue...")


def view_available_seats(seat_map):
    """Display all available seats"""
    available = seat_map.get_available_seats()
    
    print("\n" + "="*50)
    print("AVAILABLE SEATS".center(50))
    print("="*50)
    
    if available:
        print(f"\nTotal available: {len(available)} seats\n")
        # Display in rows of 10
        for i in range(0, len(available), 10):
            print("  ".join(available[i:i+10]))
    else:
        print("\n❌ No seats available - fully booked!")
    
    print("\n" + "="*50)
    input("\nPress Enter to continue...")


def view_bookings(seat_map):
    """Display all current bookings"""
    print("\n" + "="*50)
    print("CURRENT BOOKINGS".center(50))
    print("="*50)
    
    if not seat_map.bookings:
        print("\n❌ No bookings yet!")
    else:
        print(f"\nTotal bookings: {len(seat_map.bookings)}\n")
        print(f"{'Seat':<6} {'Passenger':<25} {'Booked At':<20}")
        print("-" * 50)
        for seat, info in sorted(seat_map.bookings.items()):
            print(f"{seat:<6} {info['passenger']:<25} {info['time']:<20}")
    
    print("\n" + "="*50)
    input("\nPress Enter to continue...")


def view_statistics(seat_map):
    """Display booking statistics"""
    stats = seat_map.get_statistics()
    
    print("\n" + "="*50)
    print("BOOKING STATISTICS".center(50))
    print("="*50)
    print(f"\nTotal Seats:       {stats['total']}")
    print(f"Occupied Seats:    {stats['occupied']}")
    print(f"Available Seats:   {stats['available']}")
    print(f"Occupancy Rate:    {stats['occupancy_rate']:.1f}%")
    
    # Visual representation
    print("\nOccupancy Bar:")
    occupied_blocks = int(stats['occupancy_rate'] / 2)
    available_blocks = 50 - occupied_blocks
    print("[" + "█" * occupied_blocks + "░" * available_blocks + "]")
    
    print("\n" + "="*50)
    input("\nPress Enter to continue...")


def book_stall_interactive(stall_map):
    """Interactive stall booking"""
    stall_map.display()
    
    available = stall_map.get_available_stalls()
    if not available:
        print("❌ Sorry, all stalls are fully booked!")
        input("\nPress Enter to continue...")
        return
    
    print(f"Available stalls: {len(available)}")
    print("Enter stall in format: Row+Letter (e.g., 5B, 10A)")
    
    stall_input = input("\nEnter stall to book (or 'back' to return): ")