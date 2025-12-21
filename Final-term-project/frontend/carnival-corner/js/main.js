// ===================================
// CARNIVAL CORNER - MAIN JAVASCRIPT
// ===================================

// Global state
let eventsData = [];
let locationsData = [];
let bookingsData = [];
let vendorsData = [];
let selectedSeats = [];
let currentEvent = null;

// ===================================
// DATA LOADING
// ===================================

async function loadData() {
    try {
        const [events, locations, bookings, vendors] = await Promise.all([
            fetch('./data/events.json').then(res => res.json()),
            fetch('./data/locations.json').then(res => res.json()),
            fetch('./data/bookings.json').then(res => res.json()),
            fetch('./data/vendors.json').then(res => res.json())
        ]);

        eventsData = events;
        locationsData = locations;
        bookingsData = bookings;
        vendorsData = vendors;

        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// ===================================
// NAVIGATION
// ===================================

function initNavigation() {
    const header = document.querySelector('.header');
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Active link highlighting
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// ===================================
// LOCAL STORAGE HELPERS
// ===================================

function saveToLocalStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

function getFromLocalStorage(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// ===================================
// EVENT FILTERING
// ===================================

function filterEventsByCity(city) {
    return eventsData.filter(event => event.city === city);
}

function filterEventsByArea(city, area) {
    return eventsData.filter(event => event.city === city && event.area === area);
}

function getEventById(id) {
    return eventsData.find(event => event.id === parseInt(id));
}

// ===================================
// SEATING FUNCTIONS
// ===================================

function generateSeatId(row, col) {
    const rowLetter = String.fromCharCode(65 + row); // A, B, C, etc.
    return `${rowLetter}${col + 1}`;
}

function isSeatBooked(seatId, eventId) {
    const event = getEventById(eventId);
    return event && event.seating.bookedSeats.includes(seatId);
}

function isSeatSelected(seatId) {
    return selectedSeats.includes(seatId);
}

function toggleSeatSelection(seatId, eventId) {
    if (isSeatBooked(seatId, eventId)) {
        return false; // Can't select booked seats
    }

    const index = selectedSeats.indexOf(seatId);
    if (index > -1) {
        selectedSeats.splice(index, 1);
    } else {
        selectedSeats.push(seatId);
    }

    return true;
}

function renderSeatMap(containerId, eventId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const event = getEventById(eventId);
    if (!event) return;

    const { rows, seatsPerRow } = event.seating;

    let html = '<div class="seat-map">';
    html += '<div class="screen">STAGE / SCREEN</div>';

    for (let row = 0; row < rows; row++) {
        html += '<div class="seat-row">';
        html += `<span class="row-label">${String.fromCharCode(65 + row)}</span>`;

        for (let col = 0; col < seatsPerRow; col++) {
            const seatId = generateSeatId(row, col);
            const isBooked = isSeatBooked(seatId, eventId);
            const isSelected = isSeatSelected(seatId);

            let seatClass = 'seat';
            if (isBooked) {
                seatClass += ' seat-booked';
            } else if (isSelected) {
                seatClass += ' seat-selected';
            } else {
                seatClass += ' seat-available';
            }

            html += `<button class="seat ${seatClass}" data-seat="${seatId}" ${isBooked ? 'disabled' : ''}>
                ${col + 1}
              </button>`;
        }

        html += '</div>';
    }

    html += '</div>';

    // Legend
    html += `
    <div class="seat-legend">
      <div class="legend-item">
        <div class="seat seat-available"></div>
        <span>Available</span>
      </div>
      <div class="legend-item">
        <div class="seat seat-selected"></div>
        <span>Selected</span>
      </div>
      <div class="legend-item">
        <div class="seat seat-booked"></div>
        <span>Booked</span>
      </div>
    </div>
  `;

    container.innerHTML = html;

    // Add click listeners
    container.querySelectorAll('.seat:not(.seat-booked)').forEach(seat => {
        seat.addEventListener('click', () => {
            const seatId = seat.getAttribute('data-seat');
            toggleSeatSelection(seatId, eventId);
            renderSeatMap(containerId, eventId);
            updateBookingSummary();
        });
    });
}

function updateBookingSummary() {
    const summaryElement = document.getElementById('booking-summary');
    if (!summaryElement || !currentEvent) return;

    const totalAmount = selectedSeats.length * currentEvent.price;

    summaryElement.innerHTML = `
    <h3>Booking Summary</h3>
    <p><strong>Event:</strong> ${currentEvent.name}</p>
    <p><strong>Selected Seats:</strong> ${selectedSeats.join(', ') || 'None'}</p>
    <p><strong>Number of Tickets:</strong> ${selectedSeats.length}</p>
    <p><strong>Price per Ticket:</strong> Rs. ${currentEvent.price.toLocaleString()}</p>
    <p class="total-amount"><strong>Total Amount:</strong> Rs. ${totalAmount.toLocaleString()}</p>
  `;
}

// ===================================
// BOOKING FUNCTIONS
// ===================================

function createBooking(eventId, userName, userEmail) {
    if (selectedSeats.length === 0) {
        alert('Please select at least one seat');
        return false;
    }

    const event = getEventById(eventId);
    const newBooking = {
        id: bookingsData.length + 1,
        eventId: eventId,
        userName: userName,
        userEmail: userEmail,
        seats: [...selectedSeats],
        totalAmount: selectedSeats.length * event.price,
        bookingDate: new Date().toISOString(),
        status: 'confirmed'
    };

    bookingsData.push(newBooking);

    // Update event's booked seats
    event.seating.bookedSeats.push(...selectedSeats);

    // Save to localStorage (simulating backend)
    saveToLocalStorage('bookings', bookingsData);
    saveToLocalStorage('events', eventsData);

    // Clear selected seats
    selectedSeats = [];

    return newBooking;
}

// ===================================
// ADMIN FUNCTIONS
// ===================================

function addEvent(eventData) {
    const newEvent = {
        id: eventsData.length + 1,
        ...eventData,
        seating: {
            rows: eventData.rows || 10,
            seatsPerRow: eventData.seatsPerRow || 10,
            bookedSeats: []
        }
    };

    eventsData.push(newEvent);
    saveToLocalStorage('events', eventsData);
    return newEvent;
}

function updateEvent(eventId, updatedData) {
    const index = eventsData.findIndex(e => e.id === eventId);
    if (index > -1) {
        eventsData[index] = { ...eventsData[index], ...updatedData };
        saveToLocalStorage('events', eventsData);
        return true;
    }
    return false;
}

function deleteEvent(eventId) {
    const index = eventsData.findIndex(e => e.id === eventId);
    if (index > -1) {
        eventsData.splice(index, 1);
        saveToLocalStorage('events', eventsData);
        return true;
    }
    return false;
}

// ===================================
// VENDOR FUNCTIONS
// ===================================

function registerVendor(vendorData) {
    const newVendor = {
        id: vendorsData.length + 1,
        ...vendorData,
        registrationDate: new Date().toISOString(),
        status: 'pending'
    };

    vendorsData.push(newVendor);
    saveToLocalStorage('vendors', vendorsData);
    return newVendor;
}

// ===================================
// ANIMATION UTILITIES
// ===================================

function animateOnScroll() {
    const elements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
}

// ===================================
// INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    initNavigation();
    animateOnScroll();

    // Check for saved data in localStorage
    const savedEvents = getFromLocalStorage('events');
    const savedBookings = getFromLocalStorage('bookings');
    const savedVendors = getFromLocalStorage('vendors');

    if (savedEvents) eventsData = savedEvents;
    if (savedBookings) bookingsData = savedBookings;
    if (savedVendors) vendorsData = savedVendors;

    console.log('Carnival Corner initialized!');
});

// ===================================
// UTILITY FUNCTIONS
// ===================================

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
}
