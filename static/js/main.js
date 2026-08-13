// ============================================================
// SPCart — Main JavaScript
// ============================================================

// ── Global CSRF Token Helper ──────────────────────────────────
function getCsrfToken() {
  const metaToken = document.querySelector('meta[name="csrf-token"]');
  if (metaToken && metaToken.content) {
    return metaToken.content;
  }
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('csrftoken=')) {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  if (!cookieValue) {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) cookieValue = csrfInput.value;
  }
  return cookieValue;
}

// ── Global Live Navbar Badge Updater ──────────────────────────
window.updateNavbarCounts = function (cartCount, wishlistCount) {
  if (cartCount !== undefined && cartCount !== null) {
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = cartCount;
      el.style.display = cartCount > 0 ? 'inline-block' : 'none';
    });
  }
  if (wishlistCount !== undefined && wishlistCount !== null) {
    document.querySelectorAll('.wishlist-count').forEach(el => {
      el.textContent = wishlistCount;
      el.style.display = wishlistCount > 0 ? 'inline-block' : 'none';
    });
  }
};

// ── Global Toast Notification ─────────────────────────────────
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

  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }

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

// ── Global Add to Cart Function ──────────────────────────────
window.addToCart = function (productId, event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  if (!productId) return;

  const btn = (event && (event.currentTarget || event.target)) 
    ? (event.currentTarget || event.target).closest('.btn-add-cart')
    : document.querySelector(`.btn-add-cart[data-product-id="${productId}"]`);

  const qtyInput = document.getElementById(`qty-${productId}`);
  const quantity = qtyInput ? qtyInput.value : 1;

  let originalHTML = '';
  if (btn) {
    originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
    btn.disabled = true;
  }

  const csrfToken = getCsrfToken();

  fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest'
    },
    credentials: 'same-origin',
    body: `quantity=${quantity}`
  })
  .then(async res => {
    const contentType = res.headers.get('content-type');
    if (!res.ok) {
      const errorText = await res.text();
      console.error(`Add to Cart Server Error (HTTP ${res.status} ${res.statusText}):`, errorText);
      throw new Error(`Server returned HTTP ${res.status} (${res.statusText})`);
    }
    if (contentType && contentType.includes('application/json')) {
      return res.json();
    }
    const text = await res.text();
    console.error('Non-JSON response received from server:', text);
    throw new Error('Server returned invalid non-JSON response');
  })
  .then(data => {
    if (btn) {
      btn.innerHTML = originalHTML;
      btn.disabled = false;
    }

    if (data.status === 'success' || data.success) {
      if (data.cart_count !== undefined) {
        window.updateNavbarCounts(data.cart_count, null);
      }
      window.showToast(data.message || 'Product added to cart!', 'success');
    } else {
      window.showToast(data.message || 'Could not add product to cart.', 'danger');
    }
  })
  .catch(err => {
    console.error('Add to Cart Error:', err);
    if (btn) {
      btn.innerHTML = originalHTML;
      btn.disabled = false;
    }
    window.showToast(err.message || 'Error adding product to cart.', 'danger');
  });
};

// ── Global Wishlist Toggle Function ───────────────────────────
window.toggleWishlist = function (productId, event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  if (!productId) return;

  const btn = (event && (event.currentTarget || event.target))
    ? (event.currentTarget || event.target).closest('.btn-wishlist, .btn-wishlist-toggle, .wishlist-btn')
    : document.querySelector(`[data-product-id="${productId}"]`);

  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success' || data.success) {
      if (data.wishlist_count !== undefined) {
        window.updateNavbarCounts(null, data.wishlist_count);
      }
      if (btn) {
        const icon = btn.querySelector('i');
        if (icon) {
          icon.className = (data.added || data.in_wishlist) ? 'fas fa-heart text-danger' : 'far fa-heart';
        }
      }
      window.showToast(data.message || 'Wishlist updated!', 'info');
    } else {
      window.showToast(data.message || 'Please login to add items to wishlist.', 'warning');
    }
  })
  .catch(err => {
    console.error('Wishlist Error:', err);
    window.showToast('Error updating wishlist.', 'danger');
  });
};

document.addEventListener('DOMContentLoaded', function () {

  // ── Global Event Delegation ────────────────────────────────
  document.addEventListener('click', function (e) {
    const addCartBtn = e.target.closest('.btn-add-cart');
    if (addCartBtn) {
      const pid = addCartBtn.getAttribute('data-product-id');
      if (pid) {
        window.addToCart(pid, e);
      }
      return;
    }

    const wishlistBtn = e.target.closest('.btn-wishlist, .btn-wishlist-toggle, .wishlist-btn');
    if (wishlistBtn) {
      const pid = wishlistBtn.getAttribute('data-product-id');
      if (pid) {
        window.toggleWishlist(pid, e);
      }
      return;
    }
  });

  // ── Real-Time Search Autocomplete ───────────────────────────
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

});
