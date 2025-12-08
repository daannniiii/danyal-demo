class SeatMap:
    def __init__(self, rows, seats_per_row):
        self.rows = rows
        self.seats_per_row = seats_per_row
        # Create seat map with all seats available (True = available, False = occupied)
        self.seats = [[True for _ in range(seats_per_row)] for _ in range(rows)]
    
    def book_seat(self, row, seat):
        """Book a seat (mark as occupied)"""
        if 0 <= row < self.rows and 0 <= seat < self.seats_per_row:
            if self.seats[row][seat]:
                self.seats[row][seat] = False
                return True
            else:
                print(f"Seat {row+1}{chr(65+seat)} is already occupied!")
                return False
        else:
            print("Invalid seat!")
            return False
    
    def display(self):
        """Display the seat map"""
        print("\n" + "="*50)
        print("SEAT MAP")
        print("="*50)
        print("[X] = Occupied  [ ] = Available")
        print("="*50 + "\n")
        
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


# Example usage
if __name__ == "__main__":
    # Create a seat map with 10 rows and 6 seats per row
    seat_map = SeatMap(rows=10, seats_per_row=6)
    
    # Book some seats
    seat_map.book_seat(0, 1)  # Row 1, Seat B
    seat_map.book_seat(0, 4)  # Row 1, Seat E
    seat_map.book_seat(2, 2)  # Row 3, Seat C
    seat_map.book_seat(5, 0)  # Row 6, Seat A
    seat_map.book_seat(5, 5)  # Row 6, Seat F
    seat_map.book_seat(8, 3)  # Row 9, Seat D
    
    # Display the seat map
    seat_map.display()