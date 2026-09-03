/**
 * Event Detail page — loads event info and handles booking.
 */

let currentEvent = null;
let quantity = 1;

function getEventIdFromURL() {
  // URL is /event/<id>/
  const parts = window.location.pathname.split('/').filter(Boolean);
  return parseInt(parts[parts.length - 1]);
}

function renderEvent(event) {
  currentEvent = event;

  // Image / placeholder
  const imgWrap = document.getElementById('eventImageWrap');
  if (event.image_url) {
    imgWrap.innerHTML = `<img src="${event.image_url}" alt="${event.title}" class="event-hero-image">`;
  } else {
    const catClass = getCategoryClass(event.category);
    const emoji    = getCategoryEmoji(event.category);
    imgWrap.innerHTML = `<div class="event-hero-placeholder ${catClass}">${emoji}</div>`;
  }

  document.getElementById('eventTitle').textContent = event.title;
  document.getElementById('eventDesc').textContent  = event.description;
  document.getElementById('eventCategory').textContent = event.category_display || event.category;
  document.getElementById('eventDate').textContent     = formatDate(event.date);
  document.getElementById('eventTime').textContent     = formatTime(event.time);
  document.getElementById('eventLocation').textContent = event.location;
  document.getElementById('eventPrice').textContent    = formatPrice(event.price);
  document.getElementById('eventTickets').textContent  = `${event.available_tickets} left`;

  // Booking card
  document.getElementById('bookingPrice').textContent   = formatPrice(event.price);
  document.getElementById('ticketPrice').textContent    = formatPrice(event.price);
  document.getElementById('bookingTicketsLeft').textContent = `${event.available_tickets} available`;

  if (event.is_sold_out) {
    document.getElementById('bookingForm').innerHTML =
      '<div class="empty-state"><div class="icon">😔</div><h3>Sold Out</h3><p>No tickets available for this event.</p></div>';
  }

  updateBookingSummary();
  document.title = `${event.title} | EventHub`;
}

function updateBookingSummary() {
  if (!currentEvent) return;
  const total = currentEvent.price * quantity;
  document.getElementById('qtyDisplay').textContent   = quantity;
  document.getElementById('summaryQty').textContent   = quantity;
  document.getElementById('summaryTotal').textContent = formatPrice(total);
}

async function loadEvent() {
  const id = getEventIdFromURL();
  if (!id) { window.location.href = '/'; return; }

  const { ok, data } = await apiGetEvent(id);
  if (!ok) {
    showToast('Event not found.', 'error');
    window.location.href = '/';
    return;
  }
  renderEvent(data);
}

async function handleBooking() {
  if (!isLoggedIn()) {
    window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
    return;
  }

  const btn = document.getElementById('bookBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="loading-spinner"></span> Booking...';

  const { ok, data } = await apiCreateBooking(currentEvent.id, quantity);
  btn.disabled = false;
  btn.textContent = 'Book Tickets';

  if (ok) {
    showToast(`🎉 Booked! Reference: ${data.booking_reference}`, 'success');
    // Reload the event to show updated ticket count
    setTimeout(loadEvent, 1000);
    // Show success modal
    showBookingSuccess(data);
  } else {
    const msg = data.detail || data.quantity?.[0] || data.non_field_errors?.[0] || 'Booking failed.';
    showToast(msg, 'error');
  }
}

function showBookingSuccess(booking) {
  const modal = document.getElementById('successModal');
  if (!modal) return;
  document.getElementById('successRef').textContent   = booking.booking_reference;
  document.getElementById('successEvent').textContent = booking.event_title;
  document.getElementById('successQty').textContent   = booking.quantity;
  document.getElementById('successTotal').textContent = formatPrice(booking.total_price);
  modal.classList.add('open');
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateNav();
  loadEvent();

  // Quantity controls
  document.getElementById('qtyMinus')?.addEventListener('click', () => {
    if (quantity > 1) { quantity--; updateBookingSummary(); }
  });

  document.getElementById('qtyPlus')?.addEventListener('click', () => {
    const max = currentEvent?.available_tickets || 1;
    if (quantity < max && quantity < 10) { quantity++; updateBookingSummary(); }
  });

  document.getElementById('bookBtn')?.addEventListener('click', handleBooking);

  // Close success modal
  document.getElementById('closeSuccessModal')?.addEventListener('click', () => {
    document.getElementById('successModal')?.classList.remove('open');
  });

  document.getElementById('viewDashboardBtn')?.addEventListener('click', () => {
    window.location.href = '/dashboard/';
  });

  // Mobile nav toggle
  document.getElementById('hamburger')?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  document.getElementById('logoutBtn')?.addEventListener('click', apiLogout);
});
