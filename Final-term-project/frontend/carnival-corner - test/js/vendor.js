// Vendor JavaScript
function loadEventOptions() {
    const select = document.getElementById('vendor-event');

    eventsData.forEach(event => {
        const option = document.createElement('option');
        option.value = event.id;
        option.textContent = `${event.name} - ${event.city} (${event.date})`;
        select.appendChild(option);
    });
}

document.getElementById('vendor-form').addEventListener('submit', (e) => {
    e.preventDefault();

    const vendorData = {
        vendorName: document.getElementById('vendor-name').value,
        contactPerson: document.getElementById('contact-person').value,
        email: document.getElementById('vendor-email').value,
        phone: document.getElementById('vendor-phone').value,
        stallType: document.getElementById('stall-type').value,
        eventId: parseInt(document.getElementById('vendor-event').value),
        additionalInfo: document.getElementById('vendor-info').value
    };

    registerVendor(vendorData);

    document.getElementById('vendor-form').reset();
    document.getElementById('success-modal').classList.add('active');
});

function closeSuccessModal() {
    document.getElementById('success-modal').classList.remove('active');
    window.location.href = '../index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        loadEventOptions();
    }, 200);
});
