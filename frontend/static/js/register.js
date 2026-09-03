/**
 * Registration page — handles form submission.
 */

document.addEventListener('DOMContentLoaded', () => {
  if (isLoggedIn()) window.location.href = '/';

  const form  = document.getElementById('registerForm');
  const alert = document.getElementById('registerAlert');
  const btn   = document.getElementById('registerBtn');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    alert.className = 'alert';

    const payload = {
      first_name: document.getElementById('firstName').value.trim(),
      last_name:  document.getElementById('lastName').value.trim(),
      email:      document.getElementById('email').value.trim(),
      phone:      document.getElementById('phone').value.trim(),
      password:   document.getElementById('password').value,
      password2:  document.getElementById('password2').value,
    };

    // Basic client-side validation (the real validation is server-side)
    if (!payload.first_name || !payload.last_name || !payload.email || !payload.password) {
      alert.textContent = 'Please fill in all required fields.';
      alert.className = 'alert alert-error show';
      return;
    }

    if (payload.password !== payload.password2) {
      alert.textContent = 'Passwords do not match.';
      alert.className = 'alert alert-error show';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span class="loading-spinner"></span> Creating account...';

    const { ok, data } = await apiRegister(payload);

    btn.disabled = false;
    btn.textContent = 'Create Account';

    if (ok) {
      showToast('Account created! Welcome to EventHub 🎉', 'success');
      setTimeout(() => window.location.href = '/', 600);
    } else {
      // Collect all field errors from DRF response
      const errors = [];
      for (const [field, msgs] of Object.entries(data)) {
        errors.push(Array.isArray(msgs) ? msgs.join(' ') : msgs);
      }
      alert.textContent = errors.join(' | ') || 'Registration failed.';
      alert.className = 'alert alert-error show';
    }
  });
});
