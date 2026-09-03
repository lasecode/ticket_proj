/**
 * User Dashboard — shows profile info, upcoming and past bookings.
 */

let bookings = [];
let activeTab = 'upcoming';

async function loadProfile() {
  const { ok, data } = await apiGetProfile();
  if (!ok) return;

  document.getElementById('profileName').textContent   = data.full_name || data.email;
  document.getElementById('profileEmail').textContent  = data.email;
  document.getElementById('profilePhone').textContent  = data.phone || 'Not set';
  document.getElementById('profileJoined').textContent = formatDate(data.date_joined);
  document.getElementById('profileBookings').textContent = data.total_bookings;
}

async function loadBookings() {
  const { ok, data } = await apiGetBookings();
  if (!ok) { showToast('Failed to load bookings.', 'error'); return; }
  bookings = data.results || data;
  renderBookings();
}

function renderBookings() {
  const now = new Date();
  const upcoming = bookings.filter(b => b.status === 'confirmed' && new Date(b.event_date) >= now);
  const past     = bookings.filter(b => b.status === 'cancelled'  || new Date(b.event_date) <  now);

  document.getElementById('upcomingCount').textContent = upcoming.length;
  document.getElementById('pastCount').textContent     = past.length;

  const list = activeTab === 'upcoming' ? upcoming : past;
  const container = document.getElementById('bookingsList');

  if (!list.length) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">🎫</div>
        <h3>No ${activeTab} bookings</h3>
        <p>${activeTab === 'upcoming' ? 'Browse events and book your first ticket!' : 'Your past bookings will appear here.'}</p>
        ${activeTab === 'upcoming' ? '<a href="/" class="btn btn-primary mt-2">Browse Events</a>' : ''}
      </div>`;
    return;
  }

  container.innerHTML = list.map(b => buildBookingItem(b)).join('');

  // Attach cancel listeners
  container.querySelectorAll('.cancel-btn').forEach(btn => {
    btn.addEventListener('click', () => confirmCancel(parseInt(btn.dataset.id)));
  });
}

function buildBookingItem(b) {
  const emoji = getCategoryEmoji(b.event_category);
  const canCancel = b.status === 'confirmed';

  return `
    <div class="booking-item">
      <div class="booking-icon">${emoji}</div>
      <div class="booking-info">
        <h4>${b.event_title}</h4>
        <div class="booking-ref">${b.booking_reference}</div>
        <div class="meta-item mt-1"><span class="icon">📅</span>${formatDate(b.event_date)}</div>
      </div>
      <div class="booking-meta">
        <div>
          <div style="font-size:0.75rem;color:var(--text-muted)">Tickets</div>
          <div style="font-weight:700">${b.quantity}</div>
        </div>
        <div>
          <div style="font-size:0.75rem;color:var(--text-muted)">Total</div>
          <div style="font-weight:700">${formatPrice(b.total_price)}</div>
        </div>
        <span class="status-badge status-${b.status}">${b.status_display}</span>
        ${canCancel
          ? `<button class="btn btn-danger btn-sm cancel-btn" data-id="${b.id}">Cancel</button>`
          : ''}
      </div>
    </div>`;
}

function confirmCancel(bookingId) {
  const modal = document.getElementById('cancelModal');
  modal.classList.add('open');
  document.getElementById('confirmCancelBtn').onclick = () => cancelBooking(bookingId);
}

async function cancelBooking(bookingId) {
  const modal = document.getElementById('cancelModal');
  modal.classList.remove('open');

  const { ok, data } = await apiCancelBooking(bookingId);
  if (ok) {
    showToast('Booking cancelled. Tickets returned.', 'success');
    loadBookings();
    loadProfile();
  } else {
    showToast(data.detail || 'Cancellation failed.', 'error');
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  updateNav();
  loadProfile();
  loadBookings();

  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeTab = btn.dataset.tab;
      renderBookings();
    });
  });

  // Cancel modal
  document.getElementById('closeCancelModal')?.addEventListener('click', () => {
    document.getElementById('cancelModal').classList.remove('open');
  });

  document.getElementById('hamburger')?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  document.getElementById('logoutBtn')?.addEventListener('click', apiLogout);
});
