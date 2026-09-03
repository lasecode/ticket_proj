/**
 * EventHub — API Utility Module
 * Handles all communication with the Django REST API.
 */

const API_BASE = '/api';

// ── Token Management ──────────────────────────────────────────────────────────

function getAccessToken()  { return localStorage.getItem('access_token'); }
function getRefreshToken() { return localStorage.getItem('refresh_token'); }

function saveTokens(access, refresh) {
  localStorage.setItem('access_token', access);
  if (refresh) localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
}

function saveUser(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
}

function isLoggedIn() { return !!getAccessToken(); }

// ── HTTP Request Helper ───────────────────────────────────────────────────────

async function request(method, endpoint, data = null, requireAuth = false) {
  const headers = { 'Content-Type': 'application/json' };

  if (requireAuth || getAccessToken()) {
    headers['Authorization'] = `Bearer ${getAccessToken()}`;
  }

  const options = { method, headers };
  if (data) options.body = JSON.stringify(data);

  let response = await fetch(`${API_BASE}${endpoint}`, options);

  // If 401 and we have a refresh token, try to renew the access token once
  if (response.status === 401 && getRefreshToken()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${getAccessToken()}`;
      response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    } else {
      // Refresh failed — force logout
      clearTokens();
      window.location.href = '/login/';
      return null;
    }
  }

  return response;
}

async function refreshAccessToken() {
  try {
    const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: getRefreshToken() }),
    });
    if (res.ok) {
      const data = await res.json();
      saveTokens(data.access, data.refresh);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

// ── Auth API ──────────────────────────────────────────────────────────────────

async function apiRegister(payload) {
  const res = await request('POST', '/auth/register/', payload);
  const data = await res.json();
  if (res.ok) {
    saveTokens(data.access, data.refresh);
    saveUser(data.user);
  }
  return { ok: res.ok, status: res.status, data };
}

async function apiLogin(email, password) {
  const res = await request('POST', '/auth/login/', { email, password });
  const data = await res.json();
  if (res.ok) {
    saveTokens(data.access, data.refresh);
    saveUser(data.user);
  }
  return { ok: res.ok, status: res.status, data };
}

function apiLogout() {
  clearTokens();
  window.location.href = '/';
}

async function apiGetProfile() {
  const res = await request('GET', '/auth/profile/', null, true);
  const data = await res.json();
  return { ok: res.ok, data };
}

// ── Events API ────────────────────────────────────────────────────────────────

async function apiGetEvents(params = {}) {
  const qs = new URLSearchParams(params).toString();
  const res = await request('GET', `/events/${qs ? '?' + qs : ''}`);
  const data = await res.json();
  return { ok: res.ok, data };
}

async function apiGetEvent(id) {
  const res = await request('GET', `/events/${id}/`);
  const data = await res.json();
  return { ok: res.ok, data };
}

async function apiCreateEvent(payload) {
  const res = await request('POST', '/events/', payload, true);
  const data = await res.json();
  return { ok: res.ok, status: res.status, data };
}

async function apiUpdateEvent(id, payload) {
  const res = await request('PATCH', `/events/${id}/`, payload, true);
  const data = await res.json();
  return { ok: res.ok, status: res.status, data };
}

async function apiDeleteEvent(id) {
  const res = await request('DELETE', `/events/${id}/`, null, true);
  return { ok: res.ok, status: res.status };
}

async function apiGetCategories() {
  const res = await request('GET', '/events/categories/');
  const data = await res.json();
  return { ok: res.ok, data };
}

// ── Bookings API ──────────────────────────────────────────────────────────────

async function apiGetBookings() {
  const res = await request('GET', '/bookings/', null, true);
  const data = await res.json();
  return { ok: res.ok, data };
}

async function apiCreateBooking(eventId, quantity) {
  const res = await request('POST', '/bookings/', { event: eventId, quantity }, true);
  const data = await res.json();
  return { ok: res.ok, status: res.status, data };
}

async function apiCancelBooking(bookingId) {
  const res = await request('DELETE', `/bookings/${bookingId}/`, null, true);
  const data = await res.json();
  return { ok: res.ok, data };
}

// ── Admin Stats API ───────────────────────────────────────────────────────────

async function apiGetStats() {
  const res = await request('GET', '/stats/', null, true);
  const data = await res.json();
  return { ok: res.ok, data };
}

// ── UI Helpers ────────────────────────────────────────────────────────────────

function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-NG', {
    weekday: 'short', year: 'numeric', month: 'long', day: 'numeric',
  });
}

function formatTime(timeStr) {
  if (!timeStr) return '—';
  const [h, m] = timeStr.split(':');
  const d = new Date();
  d.setHours(parseInt(h), parseInt(m));
  return d.toLocaleTimeString('en-NG', { hour: '2-digit', minute: '2-digit' });
}

function formatPrice(amount) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN', minimumFractionDigits: 0 }).format(amount);
}

function formatDateTime(dtStr) {
  if (!dtStr) return '—';
  return new Date(dtStr).toLocaleDateString('en-NG', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

const CATEGORY_EMOJI = {
  concert: '🎵', technology: '💻', business: '💼',
  sports: '⚽', education: '📚', entertainment: '🎭',
};

function getCategoryEmoji(cat) {
  return CATEGORY_EMOJI[cat?.toLowerCase()] || '🎫';
}

function getCategoryClass(cat) {
  return `cat-${cat?.toLowerCase() || 'entertainment'}`;
}

function buildEventCardHTML(event) {
  const emoji    = getCategoryEmoji(event.category);
  const catClass = getCategoryClass(event.category);
  const imgHTML  = event.image_url
    ? `<img src="${event.image_url}" alt="${event.title}" loading="lazy">`
    : `<div class="img-placeholder ${catClass}">${emoji}</div>`;

  const ticketsLeft = event.available_tickets;
  let ticketClass = '';
  if (ticketsLeft <= 5)  ticketClass = 'very-low';
  else if (ticketsLeft <= 20) ticketClass = 'low';

  const soldOutBadge = event.is_sold_out
    ? '<div class="sold-out-badge">SOLD OUT</div>' : '';

  return `
    <div class="event-card">
      <div class="event-card-image">
        ${imgHTML}
        <span class="category-tag">${event.category_display || event.category}</span>
        ${soldOutBadge}
      </div>
      <div class="event-card-body">
        <h3>${event.title}</h3>
        <div class="event-meta">
          <div class="meta-item"><span class="icon">📅</span>${formatDate(event.date)}</div>
          <div class="meta-item"><span class="icon">📍</span>${event.location}</div>
          <div class="meta-item tickets-left ${ticketClass}">
            <span class="icon">🎫</span>${ticketsLeft} ticket${ticketsLeft !== 1 ? 's' : ''} left
          </div>
        </div>
        <div class="event-card-footer">
          <div class="event-price">
            ${formatPrice(event.price)}
            <small>per ticket</small>
          </div>
          <a href="/event/${event.id}/" class="btn btn-primary btn-sm">View Event</a>
        </div>
      </div>
    </div>
  `;
}

// Update nav based on auth state
function updateNav() {
  const user = getUser();
  const loginBtn    = document.getElementById('navLoginBtn');
  const registerBtn = document.getElementById('navRegisterBtn');
  const userMenu    = document.getElementById('navUserMenu');
  const userName    = document.getElementById('navUserName');
  const adminLink   = document.getElementById('navAdminLink');

  if (user) {
    loginBtn?.classList.add('hidden');
    registerBtn?.classList.add('hidden');
    userMenu?.classList.remove('hidden');
    if (userName) userName.textContent = user.full_name || user.email;
    if (adminLink) {
      user.is_staff ? adminLink.classList.remove('hidden') : adminLink.classList.add('hidden');
    }
  } else {
    loginBtn?.classList.remove('hidden');
    registerBtn?.classList.remove('hidden');
    userMenu?.classList.add('hidden');
    adminLink?.classList.add('hidden');
  }
}

// Redirect if not logged in
function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
  }
}

// Redirect if not admin
function requireAdmin() {
  const user = getUser();
  if (!user || !user.is_staff) {
    showToast('Admin access required.', 'error');
    window.location.href = '/';
  }
}
