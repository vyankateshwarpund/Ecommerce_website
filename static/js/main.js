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

  // ── Real-Time Search Autocomplete ─────────────────────────
  const searchInput = document.querySelector('input[name="q"]');
  if (searchInput) {
    let autoSuggestBox = document.createElement('div');
    autoSuggestBox.className = 'search-autosuggest-box bg-white rounded-4 shadow-lg border p-2 position-absolute w-100 mt-1';
    autoSuggestBox.style.zIndex = '9999';
    autoSuggestBox.style.display = 'none';
    searchInput.parentNode.style.position = 'relative';
    searchInput.parentNode.appendChild(autoSuggestBox);

    searchInput.addEventListener('input', function () {
      const q = this.value.trim();
      if (q.length >= 2) {
        fetch(`/products/autocomplete/?q=${encodeURIComponent(q)}`)
          .then(res => res.json())
          .then(data => {
            if (data.results && data.results.length > 0) {
              autoSuggestBox.innerHTML = data.results.map(item => `
                <a href="${item.url}" class="d-flex align-items-center gap-3 p-2 text-decoration-none text-dark hover-bg-light rounded-3 border-bottom">
                  <img src="${item.image}" style="width: 40px; height: 40px; object-fit: contain;">
                  <div class="flex-grow-1 min-width-0">
                    <div class="small fw-bold text-truncate">${item.name}</div>
                    <span class="text-muted" style="font-size: 11px;">${item.category}</span>
                  </div>
                  <strong class="text-primary small">${item.price}</strong>
                </a>
              `).join('');
              autoSuggestBox.style.display = 'block';
            } else {
              autoSuggestBox.style.display = 'none';
            }
          });
      } else {
        autoSuggestBox.style.display = 'none';
      }
    });

    document.addEventListener('click', function (e) {
      if (!searchInput.contains(e.target) && !autoSuggestBox.contains(e.target)) {
        autoSuggestBox.style.display = 'none';
      }
    });
  }

  // ── Cart Quantity Buttons ─────────────────────────────────
  document.querySelectorAll('.btn-qty-minus').forEach(btn => {
    btn.addEventListener('click', function () {
      const input = this.nextElementSibling;
      if (input && input.value > 1) {
        input.value = parseInt(input.value) - 1;
        input.form.submit();
      }
    });
  });

  document.querySelectorAll('.btn-qty-plus').forEach(btn => {
    btn.addEventListener('click', function () {
      const input = this.previousElementSibling;
      if (input) {
        input.value = parseInt(input.value) + 1;
        input.form.submit();
      }
    });
  });

  // ── Add to Cart AJAX ──────────────────────────────────────
  document.querySelectorAll('.btn-add-cart').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.getAttribute('data-product-id');
      const qtyInput = document.getElementById(`qty-${productId}`);
      const quantity = qtyInput ? qtyInput.value : 1;

      fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-length-urlencoded',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: `quantity=${quantity}`
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success' || data.success) {
          const badge = document.querySelector('.cart-badge-count');
          if (badge) badge.textContent = data.cart_count;
          showToast(data.message || 'Product added to cart!', 'success');
        } else {
          showToast(data.message || 'Could not add product to cart.', 'danger');
        }
      })
      .catch(() => showToast('Error adding product to cart.', 'danger'));
    });
  });

});
