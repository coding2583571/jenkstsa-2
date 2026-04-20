/* Jenks TSA — main.js */
(function () {
  'use strict';

  // ── MOBILE NAV ─────────────────────────────────────
  const toggle = document.getElementById('nav-toggle');
  const mobileMenu = document.getElementById('nav-mobile-menu');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', mobileMenu.classList.contains('open'));
    });
  }

  // Close mobile menu on outside click
  document.addEventListener('click', (e) => {
    if (mobileMenu && mobileMenu.classList.contains('open')) {
      if (!mobileMenu.contains(e.target) && !toggle.contains(e.target)) {
        mobileMenu.classList.remove('open');
      }
    }
  });

  // ── NAV SCROLL EFFECT ──────────────────────────────
  const nav = document.getElementById('site-nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.boxShadow = window.scrollY > 10
        ? '0 2px 16px rgba(0,0,0,0.2)'
        : '0 1px 0 rgba(255,255,255,0.06)';
    }, { passive: true });
  }

  // ── CONTACT FORM ───────────────────────────────────
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = contactForm.querySelector('button[type="submit"]');
      const errEl = document.getElementById('cf-error');
      const okEl = document.getElementById('cf-success');
      btn.disabled = true;
      btn.textContent = 'Sending…';
      if (errEl) errEl.style.display = 'none';

      const fd = new FormData(contactForm);
      try {
        const res = await fetch('/contact/send/', {
          method: 'POST',
          headers: { 'X-CSRFToken': fd.get('csrfmiddlewaretoken') },
          body: fd,
        });
        const j = await res.json();
        if (j.success) {
          contactForm.reset();
          if (okEl) okEl.style.display = 'block';
        } else {
          if (errEl) { errEl.textContent = j.error; errEl.style.display = 'block'; }
        }
      } catch (err) {
        if (errEl) { errEl.textContent = 'Network error. Please try again.'; errEl.style.display = 'block'; }
      }
      btn.disabled = false;
      btn.textContent = 'Send Message';
    });
  }

  // ── LINK COMMITMENT FORM (dashboard) ───────────────
  const linkForm = document.getElementById('link-commitment-form');
  if (linkForm) {
    linkForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(linkForm);
      const errEl = document.getElementById('link-error');
      const okEl = document.getElementById('link-success');
      try {
        const res = await fetch('/accounts/link-commitment/', {
          method: 'POST',
          headers: { 'X-CSRFToken': fd.get('csrfmiddlewaretoken') },
          body: fd,
        });
        const j = await res.json();
        if (j.success) {
          if (okEl) okEl.style.display = 'block';
          if (errEl) errEl.style.display = 'none';
          linkForm.reset();
          setTimeout(() => window.location.reload(), 1500);
        } else {
          if (errEl) { errEl.textContent = j.error; errEl.style.display = 'block'; }
        }
      } catch (err) {
        if (errEl) { errEl.textContent = 'Network error.'; errEl.style.display = 'block'; }
      }
    });
  }

  // ── FLASH MESSAGES AUTO DISMISS ────────────────────
  const flashes = document.querySelectorAll('.flash-msg');
  flashes.forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity .4s';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // ── CSRF HELPER ────────────────────────────────────
  window.getCsrf = function () {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  };

})();
