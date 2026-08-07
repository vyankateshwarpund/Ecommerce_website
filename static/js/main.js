// ============================================================
// ShopSphere — Main JavaScript
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── CSRF Token Helper ──────────────────────────────────────
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrfToken = getCookie('csrftoken');

  // ── Toast Notification ────────────────────────────────────
  window.showToast = function (message, type = 'success') {
    const icons = {
      success: 'fa-circle-check',
      danger: 'fa-circle-xmark',
      warning: 'fa-triangle-exclamation',
      info: 'fa-circle-info',
    };
    const colors = {
      success: '#22C55E',
      danger: '#EF4444',
      warning: '#F59E0B',
      info: '#2563EB',
    };

    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toastEl = document.createElement('div');
    toastEl.className = 'toast toast-shopsphere show align-items-center mb-2';
    toastEl.style.borderLeftColor = colors[type] || colors.success;
    toastEl.innerHTML = `
      <div class="d-flex align-items-center p-3 gap-3">
        <i class="fas ${icons[type] || icons.success}" style="color: ${colors[type]}; font-size: 20px;"></i>
        <span style="font-size:14px; font-weight:500;">${message}</span>
        <button type="button" class="btn-close ms-auto" onclick="this.closest('.toast').remove()"></button>
      </div>`;
    toastContainer.appendChild(toastEl);
    setTimeout(() => toastEl.remove(), 4000);
  };

  function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
  }

  // Auto-dismiss Django messages as toasts
  document.querySelectorAll('.django-message').forEach(el => {
    const type = el.dataset.type || 'info';
    showToast(el.dataset.message, type);
  });

  // ── Add to Cart ────────────────────────────────────────────
  document.querySelectorAll('.btn-add-cart').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.dataset.productId;
      const quantity = document.getElementById('quantity')?.value || 1;

      fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ quantity: parseInt(quantity) }),
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            showToast(data.message || 'Added to cart!', 'success');
            updateCartCount(data.cart_count);
          } else {
            showToast(data.message || 'Could not add to cart.', 'danger');
          }
        })
        .catch(() => showToast('Something went wrong.', 'danger'));
    });
  });

  function updateCartCount(count) {
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  }

  // ── Wishlist Toggle ────────────────────────────────────────
  document.querySelectorAll('.btn-wishlist').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.dataset.productId;

      fetch(`/wishlist/toggle/${productId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            this.classList.toggle('active', data.in_wishlist);
            const icon = this.querySelector('i');
            icon.className = data.in_wishlist ? 'fas fa-heart' : 'far fa-heart';
            showToast(data.message, 'success');
            updateWishlistCount(data.wishlist_count);
          } else if (data.redirect) {
            window.location.href = data.redirect;
          }
        });
    });
  });

  function updateWishlistCount(count) {
    document.querySelectorAll('.wishlist-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  }

  // ── Quantity Selector ─────────────────────────────────────
  const qtyInput = document.getElementById('quantity');
  document.getElementById('qty-plus')?.addEventListener('click', () => {
    const max = parseInt(qtyInput.max) || 99;
    if (parseInt(qtyInput.value) < max) qtyInput.value = parseInt(qtyInput.value) + 1;
  });
  document.getElementById('qty-minus')?.addEventListener('click', () => {
    if (parseInt(qtyInput.value) > 1) qtyInput.value = parseInt(qtyInput.value) - 1;
  });

  // ── Navbar Search ─────────────────────────────────────────
  const searchInput = document.getElementById('search-input');
  searchInput?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && this.value.trim()) {
      window.location.href = `/products/?q=${encodeURIComponent(this.value.trim())}`;
    }
  });

  // ── Smooth scroll for anchor links ────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // ── Live Deals Countdown Timer (Updates every second) ────
  function startDealsCountdown() {
    let hours = 8, minutes = 42, seconds = 15;
    const hoursEl = document.getElementById('timer-hours');
    const minsEl = document.getElementById('timer-mins');
    const secsEl = document.getElementById('timer-secs');

    if (!hoursEl || !minsEl || !secsEl) return;

    setInterval(() => {
      if (seconds > 0) {
        seconds--;
      } else {
        seconds = 59;
        if (minutes > 0) {
          minutes--;
        } else {
          minutes = 59;
          if (hours > 0) hours--;
        }
      }

      hoursEl.textContent = hours.toString().padStart(2, '0');
      minsEl.textContent = minutes.toString().padStart(2, '0');
      secsEl.textContent = seconds.toString().padStart(2, '0');
    }, 1000);
  }
  startDealsCountdown();

  // ── Back to Top Button ────────────────────────────────────
  const backToTop = document.getElementById('back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.style.display = window.scrollY > 300 ? 'flex' : 'none';
    });
    backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

});
