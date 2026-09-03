/**
 * Login page — handles form submission and redirect.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Already logged in → redirect home
  if (isLoggedIn()) window.location.href = '/';

  const form    = document.getElementById('loginForm');
  const alert   = document.getElementById('loginAlert');
  const btn     = document.getElementById('loginBtn');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    alert.className = 'alert';

    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      alert.textContent = 'Please fill in all fields.';
      alert.className = 'alert alert-error show';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span class="loading-spinner"></span> Logging in...';

    const { ok, data } = await apiLogin(email, password);

    btn.disabled = false;
    btn.textContent = 'Log In';

    if (ok) {
      showToast('Welcome back! 👋', 'success');
      // Redirect: admin → admin dashboard, users → home or ?next param
      const params = new URLSearchParams(window.location.search);
      const next   = params.get('next') || (data.user?.is_staff ? '/admin-dashboard/' : '/');
      setTimeout(() => window.location.href = next, 500);
    } else {
      const msg = data.detail || data.non_field_errors?.[0] || 'Invalid email or password.';
      alert.textContent = msg;
      alert.className = 'alert alert-error show';
    }
  });
});
