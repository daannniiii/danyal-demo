// ===================================
// EVENT DETAILS PAGE JAVASCRIPT
// ===================================

let eventId = null;

// Load event details
function loadEventDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    eventId = parseInt(urlParams.get('id'));

    if (!eventId) {
        alert('Event not found');
        window.location.href = 'events.html';
        return;
    }

    currentEvent = getEventById(eventId);

    if (!currentEvent) {
        alert('Event not found');
        window.location.href = 'events.html';
        return;
    }

    displayEventInfo();
    renderSeatMap('seat-map-container', eventId);
    updateBookingSummary();
}

// Display event information
function displayEventInfo() {
    const eventInfo = document.getElementById('event-info');
    const availableSeats = currentEvent.totalSeats - currentEvent.seating.bookedSeats.length;

    eventInfo.innerHTML = `
    <div class="event-header fade-in">
      <div class="event-image-large">🎭</div>
      <div class="event-header-content">
        <span class="event-category-badge">${currentEvent.category}</span>
        <h1 class="event-title">${currentEvent.name}</h1>
        <div class="event-meta">
          <div class="event-meta-item">
            <span class="event-meta-icon">📍</span>
            <span>${currentEvent.venue}, ${currentEvent.area}, ${currentEvent.city}</span>
          </div>
          <div class="event-meta-item">
            <span class="event-meta-icon">📅</span>
            <span>${formatDate(currentEvent.date)}</span>
          </div>
          <div class="event-meta-item">
            <span class="event-meta-icon">🕐</span>
            <span>${formatTime(currentEvent.time)}</span>
          </div>
          <div class="event-meta-item">
            <span class="event-meta-icon">🪑</span>
            <span>${availableSeats} seats available</span>
          </div>
        </div>
        <div class="event-price-display">Rs. ${currentEvent.price.toLocaleString()} per ticket</div>
      </div>
    </div>
    <div class="event-description fade-in">
      <p>${currentEvent.description}</p>
    </div>
  `;
}

// Confirm booking
function confirmBooking() {
    const userName = document.getElementById('user-name').value.trim();
    const userEmail = document.getElementById('user-email').value.trim();
    const userPhone = document.getElementById('user-phone').value.trim();

    // Validation
    if (!userName) {
        alert('Please enter your name');
        return;
    }

    if (!userEmail) {
        alert('Please enter your email');
        return;
    }

    if (!userPhone) {
        alert('Please enter your phone number');
        return;
    }

    if (selectedSeats.length === 0) {
        alert('Please select at least one seat');
        return;
    }

    // Create booking
    const booking = createBooking(eventId, userName, userEmail);

    if (booking) {
        showConfirmationModal(booking, userName, userEmail);

        // Re-render seat map to show updated booked seats
        renderSeatMap('seat-map-container', eventId);

        // Clear form
        document.getElementById('user-name').value = '';
        document.getElementById('user-email').value = '';
        document.getElementById('user-phone').value = '';
    }
}

// Show confirmation modal
function showConfirmationModal(booking, userName, userEmail) {
    const modal = document.getElementById('booking-modal');
    const modalBody = document.getElementById('modal-body');

    modalBody.innerHTML = `
    <p><strong>Booking ID:</strong> #${booking.id.toString().padStart(6, '0')}</p>
    <p><strong>Name:</strong> ${userName}</p>
    <p><strong>Email:</strong> ${userEmail}</p>
    <p><strong>Event:</strong> ${currentEvent.name}</p>
    <p><strong>Date:</strong> ${formatDate(currentEvent.date)} at ${formatTime(currentEvent.time)}</p>
    <p><strong>Venue:</strong> ${currentEvent.venue}, ${currentEvent.area}, ${currentEvent.city}</p>
    <p><strong>Seats:</strong> ${booking.seats.join(', ')}</p>
    <p><strong>Total Amount:</strong> Rs. ${booking.totalAmount.toLocaleString()}</p>
    <hr style="border-color: rgba(167, 157, 218, 0.2); margin: 1rem 0;">
    <p style="color: var(--golden-yellow); text-align: center;">
      A confirmation email has been sent to ${userEmail}
    </p>
  `;

    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('booking-modal');
    modal.classList.remove('active');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        loadEventDetails();
    }, 200);

    // Close modal on outside click
    document.getElementById('booking-modal').addEventListener('click', (e) => {
        if (e.target.id === 'booking-modal') {
            closeModal();
        }
    });
});
