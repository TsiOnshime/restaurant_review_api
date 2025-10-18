// Minimal front-end to interact with your API.
// API base assumes the Django app serves /api/
const API_BASE = '/api';
let token = localStorage.getItem('token') || null;

const els = {
  username: document.getElementById('username'),
  password: document.getElementById('password'),
  btnLogin: document.getElementById('btn-login'),
  btnLogout: document.getElementById('btn-logout'),
  status: document.getElementById('status'),
  restaurants: document.getElementById('restaurants'),
  reviews: document.getElementById('reviews'),
  reviewForm: document.getElementById('review-form'),
  reviewRestaurant: document.getElementById('review-restaurant'),
  reviewRating: document.getElementById('review-rating'),
  reviewContent: document.getElementById('review-content'),
  btnCreateReview: document.getElementById('btn-create-review'),
};

function setAuthState() {
  if (token) {
    els.status.textContent = 'Logged in';
    els.btnLogin.hidden = true;
    els.btnLogout.hidden = false;
    els.reviewForm.hidden = false;
  } else {
    els.status.textContent = 'Not logged in';
    els.btnLogin.hidden = false;
    els.btnLogout.hidden = true;
    els.reviewForm.hidden = true;
  }
}

async function login() {
  const username = els.username.value.trim();
  const password = els.password.value;
  if (!username || !password) return alert('Enter username and password');

  const res = await fetch(`${API_BASE}/auth/token/`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  if (!res.ok) {
    const err = await res.json().catch(()=>null);
    return alert('Login failed: ' + (err?.detail || res.statusText));
  }
  const data = await res.json();
  token = data.access;
  localStorage.setItem('token', token);
  setAuthState();
}

function logout() {
  token = null;
  localStorage.removeItem('token');
  setAuthState();
}

async function loadRestaurants() {
  els.restaurants.innerHTML = 'Loading...';
  const res = await fetch(`${API_BASE}/restaurants/`);
  if (!res.ok) { els.restaurants.textContent = 'Failed to load restaurants'; return; }
  const data = await res.json();
  els.restaurants.innerHTML = '';
  data.forEach(r => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <h4>${r.name} <small>(id:${r.id})</small></h4>
      <div>${r.address || ''}</div>
      <p>${r.description || ''}</p>
      <button data-id="${r.id}" class="btn-view-reviews">View reviews</button>
    `;
    els.restaurants.appendChild(card);
  });
  document.querySelectorAll('.btn-view-reviews').forEach(btn => btn.addEventListener('click', () => {
    const id = btn.dataset.id;
    els.reviewRestaurant.value = id;
    loadReviews({restaurant: id});
  }));
}

async function loadReviews(filter={}) {
  els.reviews.innerHTML = 'Loading...';
  const res = await fetch(`${API_BASE}/reviews/`);
  if (!res.ok) { els.reviews.textContent = 'Failed to load reviews'; return; }
  let data = await res.json();
  if (filter.restaurant) {
    data = data.filter(r => r.restaurant === Number(filter.restaurant));
  }
  els.reviews.innerHTML = '';
  if (!data.length) { els.reviews.textContent = 'No reviews found.'; return; }
  data.forEach(r => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <strong>${r.restaurant_name || ('Restaurant '+r.restaurant)}</strong>
      <div>By: ${r.user || 'unknown'} | Rating: ${r.rating}</div>
      <p>${r.content || ''}</p>
      <small>${new Date(r.created_at).toLocaleString()}</small>
    `;
    els.reviews.appendChild(card);
  });
}

async function createReview() {
  if (!token) return alert('Please log in to submit a review');
  const payload = {
    restaurant: Number(els.reviewRestaurant.value),
    rating: Number(els.reviewRating.value),
    comment: els.reviewContent.value.trim()    // keep 'comment' if your model uses comment
  };
  // change payload.content -> payload.comment
  if (!payload.restaurant || !payload.comment) return alert('Restaurant and content required');
  const res = await fetch(`${API_BASE}/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json().catch(()=>null);
    return alert('Error: ' + (err?.detail || JSON.stringify(err) || res.statusText));
  }
  alert('Review submitted');
  els.reviewContent.value = '';
  loadReviews({restaurant: payload.restaurant});
}

/* events */
els.btnLogin.addEventListener('click', login);
els.btnLogout.addEventListener('click', logout);
els.btnCreateReview.addEventListener('click', createReview);

setAuthState();
loadRestaurants();
loadReviews();