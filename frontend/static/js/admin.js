/**
 * Admin Dashboard — stats, event management, booking overview.
 */

let allAdminEvents = [];
let editingEventId = null;

// ── Stats ─────────────────────────────────────────────────────────────────────

async function loadStats() {
  const { ok, data } = await apiGetStats();
  if (!ok) { showToast('Failed to load stats.', 'error'); return; }

  document.getElementById('statEvents').textContent   = data.total_events;
  document.getElementById('statBookings').textContent  = data.total_bookings;
  document.getElementById('statUsers').textContent     = data.total_users;
  document.getElementById('statTickets').textContent   = data.tickets_sold;
  document.getElementById('statRevenue').textContent   = formatPrice(data.revenue);

  // Recent bookings table
  const tbody = document.getElementById('recentBookingsTbody');
  if (data.recent_bookings?.length) {
    tbody.innerHTML = data.recent_bookings.map(b => `
      <tr>
        <td><code style="color:var(--primary-light)">${b.booking_reference}</code></td>
        <td>${b.event_title}</td>
        <td>${b.quantity}</td>
        <td>${formatPrice(b.total_price)}</td>
        <td><span class="status-badge status-${b.status}">${b.status_display}</span></td>
        <td>${formatDateTime(b.booking_date)}</td>
      </tr>`).join('');
  } else {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No bookings yet.</td></tr>';
  }
}

// ── Events Table ──────────────────────────────────────────────────────────────

async function loadAdminEvents() {
  const tbody = document.getElementById('eventsTbody');
  tbody.innerHTML = '<tr><td colspan="8"><div class="skeleton" style="height:40px"></div></td></tr>';

  const { ok, data } = await apiGetEvents();
  if (!ok) { tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Failed to load events.</td></tr>'; return; }

  allAdminEvents = data.results || data;

  tbody.innerHTML = allAdminEvents.length
    ? allAdminEvents.map(e => {
        const imgThumb = e.image_url
          ? `<img src="${e.image_url}" alt="${e.title}" style="width:48px;height:36px;object-fit:cover;border-radius:6px">`
          : `<div style="width:48px;height:36px;background:var(--bg-dark);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.2rem">${getCategoryEmoji(e.category)}</div>`;
        return `
        <tr>
          <td>${imgThumb}</td>
          <td><strong style="color:var(--text-primary)">${e.title}</strong></td>
          <td><span class="category-tag" style="position:static">${e.category_display || e.category}</span></td>
          <td>${formatDate(e.date)}</td>
          <td>${e.location}</td>
          <td>${formatPrice(e.price)}</td>
          <td>
            <span style="color:${e.available_tickets < 10 ? 'var(--warning)' : 'var(--success)'}">
              ${e.available_tickets}
            </span> / ${e.total_tickets}
          </td>
          <td>
            <div class="d-flex gap-1">
              <button class="btn btn-outline btn-sm edit-event-btn" data-id="${e.id}">✏️ Edit</button>
              <button class="btn btn-danger btn-sm delete-event-btn" data-id="${e.id}">🗑️ Delete</button>
            </div>
          </td>
        </tr>`;
      }).join('')
    : '<tr><td colspan="8" class="text-center text-muted">No events found.</td></tr>';

  // Attach listeners
  tbody.querySelectorAll('.edit-event-btn').forEach(btn => {
    btn.addEventListener('click', () => openEditModal(parseInt(btn.dataset.id)));
  });
  tbody.querySelectorAll('.delete-event-btn').forEach(btn => {
    btn.addEventListener('click', () => confirmDeleteEvent(parseInt(btn.dataset.id)));
  });
}

// ── Event Modal ───────────────────────────────────────────────────────────────

function openCreateModal() {
  editingEventId = null;
  document.getElementById('eventModalTitle').textContent = 'Create Event';
  document.getElementById('eventForm').reset();
  const previewContainer = document.getElementById('imagePreviewContainer');
  if (previewContainer) previewContainer.style.display = 'none';
  document.getElementById('eventModal').classList.add('open');
}

function openEditModal(id) {
  const event = allAdminEvents.find(e => e.id === id);
  if (!event) return;

  editingEventId = id;
  document.getElementById('eventModalTitle').textContent = 'Edit Event';
  document.getElementById('eventForm').reset();

  // Populate form fields
  const fields = ['title', 'description', 'location', 'date', 'time', 'category', 'price', 'total_tickets'];
  fields.forEach(f => {
    const el = document.getElementById(`field_${f}`);
    if (el) el.value = event[f] ?? '';
  });
  document.getElementById('field_is_featured').checked = event.is_featured;

  const previewContainer = document.getElementById('imagePreviewContainer');
  const previewImg = document.getElementById('imagePreview');
  if (event.image_url && previewContainer && previewImg) {
    previewImg.src = event.image_url;
    previewContainer.style.display = 'block';
  } else if (previewContainer) {
    previewContainer.style.display = 'none';
  }

  document.getElementById('eventModal').classList.add('open');
}

async function saveEvent(e) {
  e.preventDefault();
  const btn = document.getElementById('saveEventBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="loading-spinner"></span>';

  const formData = new FormData();
  formData.append('title', document.getElementById('field_title').value.trim());
  formData.append('description', document.getElementById('field_description').value.trim());
  formData.append('location', document.getElementById('field_location').value.trim());
  formData.append('date', document.getElementById('field_date').value);
  formData.append('time', document.getElementById('field_time').value);
  formData.append('category', document.getElementById('field_category').value);
  formData.append('price', parseFloat(document.getElementById('field_price').value));
  formData.append('total_tickets', parseInt(document.getElementById('field_total_tickets').value));
  formData.append('is_featured', document.getElementById('field_is_featured').checked);

  const imageInput = document.getElementById('field_image');
  if (imageInput && imageInput.files && imageInput.files[0]) {
    formData.append('image', imageInput.files[0]);
  }

  const result = editingEventId
    ? await apiUpdateEvent(editingEventId, formData)
    : await apiCreateEvent(formData);

  btn.disabled = false;
  btn.textContent = 'Save Event';

  if (result.ok) {
    showToast(editingEventId ? 'Event updated!' : 'Event created!', 'success');
    document.getElementById('eventModal').classList.remove('open');
    loadAdminEvents();
    loadStats();
  } else {
    const errors = typeof result.data === 'object' ? Object.values(result.data).flat().join(' | ') : 'Save failed.';
    showToast(errors || 'Save failed.', 'error');
  }
}

function confirmDeleteEvent(id) {
  const modal = document.getElementById('deleteModal');
  modal.classList.add('open');
  document.getElementById('confirmDeleteBtn').onclick = () => deleteEvent(id);
}

async function deleteEvent(id) {
  document.getElementById('deleteModal').classList.remove('open');
  const { ok } = await apiDeleteEvent(id);
  if (ok) {
    showToast('Event deleted.', 'success');
    loadAdminEvents();
    loadStats();
  } else {
    showToast('Delete failed.', 'error');
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  requireAdmin();
  updateNav();
  loadStats();
  loadAdminEvents();

  document.getElementById('createEventBtn')?.addEventListener('click', openCreateModal);
  document.getElementById('eventForm')?.addEventListener('submit', saveEvent);

  document.getElementById('closeEventModal')?.addEventListener('click', () => {
    document.getElementById('eventModal').classList.remove('open');
  });
  document.getElementById('closeDeleteModal')?.addEventListener('click', () => {
    document.getElementById('deleteModal').classList.remove('open');
  });

  document.getElementById('hamburger')?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  document.getElementById('logoutBtn')?.addEventListener('click', apiLogout);
});
