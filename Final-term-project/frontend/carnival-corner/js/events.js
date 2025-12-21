// ===================================
// EVENTS PAGE JAVASCRIPT
// ===================================

let filteredEvents = [];

// Load and display events
function loadEvents() {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const urlCity = urlParams.get('city');
    const urlArea = urlParams.get('area');

    // Apply URL filters if present
    if (urlCity) {
        document.getElementById('filter-city').value = urlCity;
        updateAreaFilter(urlCity);
        if (urlArea) {
            setTimeout(() => {
                document.getElementById('filter-area').value = urlArea;
            }, 100);
        }
    }

    applyFilters();
}

// Update area filter based on selected city
function updateAreaFilter(city) {
    const areaSelect = document.getElementById('filter-area');

    if (!city) {
        areaSelect.disabled = true;
        areaSelect.innerHTML = '<option value="">Select City First</option>';
        return;
    }

    const cityData = locationsData.find(loc => loc.city === city);
    if (!cityData) return;

    areaSelect.disabled = false;
    areaSelect.innerHTML = '<option value="">All Areas</option>';

    cityData.areas.forEach(area => {
        const option = document.createElement('option');
        option.value = area;
        option.textContent = area;
        areaSelect.appendChild(option);
    });
}

// Apply filters
function applyFilters() {
    const cityFilter = document.getElementById('filter-city').value;
    const areaFilter = document.getElementById('filter-area').value;
    const categoryFilter = document.getElementById('filter-category').value;

    filteredEvents = eventsData.filter(event => {
        const matchCity = !cityFilter || event.city === cityFilter;
        const matchArea = !areaFilter || event.area === areaFilter;
        const matchCategory = !categoryFilter || event.category === categoryFilter;
        return matchCity && matchArea && matchCategory;
    });

    displayEvents();
}

// Display events
function displayEvents() {
    const eventsGrid = document.getElementById('events-grid');
    const noEvents = document.getElementById('no-events');

    if (filteredEvents.length === 0) {
        eventsGrid.style.display = 'none';
        noEvents.style.display = 'block';
        return;
    }

    eventsGrid.style.display = 'grid';
    noEvents.style.display = 'none';
    eventsGrid.innerHTML = '';

    filteredEvents.forEach(event => {
        const availableSeats = event.totalSeats - event.seating.bookedSeats.length;
        const isLimited = availableSeats <= 20;

        const eventCard = document.createElement('div');
        eventCard.className = 'event-card card fade-in';
        eventCard.onclick = () => {
            window.location.href = `event-details.html?id=${event.id}`;
        };

        eventCard.innerHTML = `
      <div class="event-image">🎭</div>
      <div class="card-content">
        <span class="event-category">${event.category}</span>
        <h3 class="event-name">${event.name}</h3>
        <div class="event-details">
          <span>📍 ${event.venue}, ${event.area}, ${event.city}</span>
          <span>📅 ${formatDate(event.date)}</span>
          <span>🕐 ${formatTime(event.time)}</span>
        </div>
        <div class="event-footer">
          <div class="event-price">Rs. ${event.price.toLocaleString()}</div>
          <div class="event-seats ${isLimited ? 'limited' : ''}">
            ${availableSeats} seats left
          </div>
        </div>
      </div>
    `;

        eventsGrid.appendChild(eventCard);
    });
}

// Reset filters
function resetFilters() {
    document.getElementById('filter-city').value = '';
    document.getElementById('filter-area').value = '';
    document.getElementById('filter-category').value = '';
    updateAreaFilter('');
    applyFilters();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        loadEvents();

        // Add filter listeners
        document.getElementById('filter-city').addEventListener('change', (e) => {
            updateAreaFilter(e.target.value);
            applyFilters();
        });

        document.getElementById('filter-area').addEventListener('change', applyFilters);
        document.getElementById('filter-category').addEventListener('change', applyFilters);
    }, 200);
});
