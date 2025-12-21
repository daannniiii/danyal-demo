// Admin JavaScript
function loadDashboard() {
    updateStats();
    loadEventsTable();
    loadVendorsTable();
}

function updateStats() {
    document.getElementById('total-events').textContent = eventsData.length;
    document.getElementById('total-bookings').textContent = bookingsData.length;
    document.getElementById('total-vendors').textContent = vendorsData.length;

    const revenue = bookingsData.reduce((sum, booking) => sum + booking.totalAmount, 0);
    document.getElementById('total-revenue').textContent = `Rs. ${revenue.toLocaleString()}`;
}

function loadEventsTable() {
    const tbody = document.getElementById('events-table-body');
    tbody.innerHTML = '';

    eventsData.forEach(event => {
        const availableSeats = event.totalSeats - event.seating.bookedSeats.length;
        const row = document.createElement('tr');
        row.innerHTML = `
      <td>${event.id}</td>
      <td>${event.name}</td>
      <td>${event.city}</td>
      <td>${event.area}</td>
      <td>${event.date}</td>
      <td>Rs. ${event.price.toLocaleString()}</td>
      <td>${availableSeats}/${event.totalSeats}</td>
      <td class="action-btns">
        <button class="btn btn-tertiary btn-sm" onclick="editEvent(${event.id})">Edit</button>
        <button class="btn btn-tertiary btn-sm" onclick="confirmDeleteEvent(${event.id})">Delete</button>
      </td>
    `;
        tbody.appendChild(row);
    });
}

function loadVendorsTable() {
    const tbody = document.getElementById('vendors-table-body');
    tbody.innerHTML = '';

    vendorsData.forEach(vendor => {
        const event = getEventById(vendor.eventId);
        const row = document.createElement('tr');
        row.innerHTML = `
      <td>${vendor.id}</td>
      <td>${vendor.vendorName}</td>
      <td>${vendor.email}</td>
      <td>${vendor.stallType}</td>
      <td>${event ? event.name : 'N/A'}</td>
      <td><span class="status-badge status-${vendor.status}">${vendor.status}</span></td>
      <td class="action-btns">
        ${vendor.status === 'pending' ? `<button class="btn btn-primary btn-sm" onclick="approveVendor(${vendor.id})">Approve</button>` : ''}
      </td>
    `;
        tbody.appendChild(row);
    });
}

function showAddEventForm() {
    document.getElementById('modal-title').textContent = 'Add New Event';
    document.getElementById('event-form').reset();
    document.getElementById('event-id').value = '';
    document.getElementById('event-modal').classList.add('active');
}

function editEvent(id) {
    const event = getEventById(id);
    if (!event) return;

    document.getElementById('modal-title').textContent = 'Edit Event';
    document.getElementById('event-id').value = event.id;
    document.getElementById('event-name').value = event.name;
    document.getElementById('event-description').value = event.description;
    document.getElementById('event-city').value = event.city;
    document.getElementById('event-area').value = event.area;
    document.getElementById('event-venue').value = event.venue;
    document.getElementById('event-date').value = event.date;
    document.getElementById('event-time').value = event.time;
    document.getElementById('event-category').value = event.category;
    document.getElementById('event-price').value = event.price;
    document.getElementById('event-rows').value = event.seating.rows;
    document.getElementById('event-seats-per-row').value = event.seating.seatsPerRow;

    document.getElementById('event-modal').classList.add('active');
}

function saveEvent() {
    const id = document.getElementById('event-id').value;
    const eventData = {
        name: document.getElementById('event-name').value,
        description: document.getElementById('event-description').value,
        city: document.getElementById('event-city').value,
        area: document.getElementById('event-area').value,
        venue: document.getElementById('event-venue').value,
        date: document.getElementById('event-date').value,
        time: document.getElementById('event-time').value,
        category: document.getElementById('event-category').value,
        price: parseInt(document.getElementById('event-price').value),
        rows: parseInt(document.getElementById('event-rows').value),
        seatsPerRow: parseInt(document.getElementById('event-seats-per-row').value),
        totalSeats: parseInt(document.getElementById('event-rows').value) * parseInt(document.getElementById('event-seats-per-row').value),
        image: 'placeholder.jpg'
    };

    if (id) {
        updateEvent(parseInt(id), eventData);
    } else {
        addEvent(eventData);
    }

    closeEventModal();
    loadDashboard();
}

function confirmDeleteEvent(id) {
    if (confirm('Are you sure you want to delete this event?')) {
        deleteEvent(id);
        loadDashboard();
    }
}

function approveVendor(id) {
    const vendor = vendorsData.find(v => v.id === id);
    if (vendor) {
        vendor.status = 'approved';
        saveToLocalStorage('vendors', vendorsData);
        loadVendorsTable();
    }
}

function closeEventModal() {
    document.getElementById('event-modal').classList.remove('active');
}

function logout() {
    window.location.href = '../index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        loadDashboard();
    }, 200);
});
