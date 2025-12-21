// ===================================
// HOME PAGE JAVASCRIPT
// ===================================

let selectedCity = null;
let selectedArea = null;

// Update city event counts
function updateCityStats() {
    const cities = ['Lahore', 'Karachi', 'Islamabad'];

    cities.forEach(city => {
        const cityEvents = filterEventsByCity(city);
        const element = document.getElementById(`${city.toLowerCase()}-events`);
        if (element) {
            element.textContent = `${cityEvents.length} Events Available`;
        }
    });
}

// Select city and show areas
function selectCity(city) {
    selectedCity = city;

    // Hide city section
    document.getElementById('city-selection').style.display = 'none';

    // Show area section
    const areaSection = document.getElementById('area-selection');
    areaSection.style.display = 'block';

    // Update breadcrumb
    document.getElementById('selected-city-breadcrumb').textContent = city;

    // Load areas for selected city
    loadAreas(city);

    // Smooth scroll to area section
    areaSection.scrollIntoView({ behavior: 'smooth' });
}

// Load areas for selected city
function loadAreas(city) {
    const cityData = locationsData.find(loc => loc.city === city);
    if (!cityData) return;

    const areaGrid = document.getElementById('area-grid');
    areaGrid.innerHTML = '';

    cityData.areas.forEach(area => {
        const events = filterEventsByArea(city, area);

        const areaCard = document.createElement('div');
        areaCard.className = 'area-card card';
        areaCard.onclick = () => selectArea(city, area);

        areaCard.innerHTML = `
      <h3 class="area-name">${area}</h3>
      <p class="area-events-count">${events.length} Event${events.length !== 1 ? 's' : ''}</p>
    `;

        areaGrid.appendChild(areaCard);
    });
}

// Select area and redirect to events page
function selectArea(city, area) {
    selectedArea = area;

    // Save to localStorage for events page
    saveToLocalStorage('selectedCity', city);
    saveToLocalStorage('selectedArea', area);

    // Redirect to events page
    window.location.href = `pages/events.html?city=${encodeURIComponent(city)}&area=${encodeURIComponent(area)}`;
}

// Reset selection
function resetSelection() {
    selectedCity = null;
    selectedArea = null;

    document.getElementById('city-selection').style.display = 'block';
    document.getElementById('area-selection').style.display = 'none';

    // Scroll to city selection
    document.getElementById('city-selection').scrollIntoView({ behavior: 'smooth' });
}

// Load featured events
function loadFeaturedEvents() {
    const featuredContainer = document.getElementById('featured-events');
    if (!featuredContainer) return;

    // Show first 3 events
    const featuredEvents = eventsData.slice(0, 3);

    featuredContainer.innerHTML = '';

    featuredEvents.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'event-card card fade-in';
        eventCard.onclick = () => {
            window.location.href = `pages/event-details.html?id=${event.id}`;
        };

        eventCard.innerHTML = `
      <div class="event-image">🎭</div>
      <div class="card-content">
        <span class="event-category">${event.category}</span>
        <h3 class="event-name">${event.name}</h3>
        <div class="event-details">
          <span>📍 ${event.venue}, ${event.area}</span>
          <span>📅 ${formatDate(event.date)}</span>
          <span>🕐 ${formatTime(event.time)}</span>
        </div>
        <div class="event-price">Rs. ${event.price.toLocaleString()}</div>
      </div>
    `;

        featuredContainer.appendChild(eventCard);
    });
}

// Initialize home page
document.addEventListener('DOMContentLoaded', () => {
    // Wait for data to load
    setTimeout(() => {
        updateCityStats();
        loadFeaturedEvents();
    }, 100);
});
