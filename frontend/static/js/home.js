/**
 * Home page — loads events, handles search/filter.
 */

let allEvents = [];
let activeCategory = '';
let searchQuery    = '';

async function loadEvents() {
  const grid = document.getElementById('eventsGrid');
  const featuredGrid = document.getElementById('featuredGrid');
  grid.innerHTML = '<div class="skeleton" style="height:300px;border-radius:12px"></div>'.repeat(3);

  const params = { upcoming: 'true' };
  if (searchQuery)   params.search   = searchQuery;
  if (activeCategory) params.category = activeCategory;

  const { ok, data } = await apiGetEvents(params);
  if (!ok) { grid.innerHTML = '<div class="empty-state"><div class="icon">⚠️</div><h3>Failed to load events</h3></div>'; return; }

  allEvents = data.results || data;

  // Featured events (top row)
  if (featuredGrid) {
    const featured = allEvents.filter(e => e.is_featured).slice(0, 4);
    if (featured.length) {
      featuredGrid.innerHTML = featured.map(buildEventCardHTML).join('');
    } else {
      document.getElementById('featuredSection')?.classList.add('hidden');
    }
  }

  // All / filtered events
  const nonFeatured = featuredGrid ? allEvents.filter(e => !e.is_featured) : allEvents;
  grid.innerHTML = nonFeatured.length
    ? nonFeatured.map(buildEventCardHTML).join('')
    : '<div class="empty-state"><div class="icon">🎫</div><h3>No events found</h3><p>Try adjusting your search or filters.</p></div>';
}

async function loadCategories() {
  const list = document.getElementById('categoryList');
  const { ok, data } = await apiGetCategories();
  if (!ok) return;

  const allBtn = `<button class="category-btn active" data-category="">All Events</button>`;
  list.innerHTML = allBtn + data.map(c =>
    `<button class="category-btn" data-category="${c.value}">${getCategoryEmoji(c.value)} ${c.label}</button>`
  ).join('');

  list.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      list.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.dataset.category;
      loadEvents();
    });
  });
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateNav();
  loadCategories();
  loadEvents();

  // Search
  const searchInput = document.getElementById('searchInput');
  let searchTimer;
  searchInput?.addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchQuery = e.target.value.trim();
    searchTimer = setTimeout(loadEvents, 400);
  });

  // Search form submit
  document.getElementById('searchForm')?.addEventListener('submit', e => {
    e.preventDefault();
    loadEvents();
  });

  // Mobile nav toggle
  document.getElementById('hamburger')?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  // Logout
  document.getElementById('logoutBtn')?.addEventListener('click', apiLogout);
});
