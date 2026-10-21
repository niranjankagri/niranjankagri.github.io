(function () {
  'use strict';
  var root = document.documentElement;
  var themeButton = document.getElementById('theme');
  var themeKey = 'na-theme';

  function currentTheme() {
    if (root.dataset.theme === 'light' || root.dataset.theme === 'dark') return root.dataset.theme;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function updateThemeButton() {
    if (!themeButton) return;
    var dark = currentTheme() === 'dark';
    themeButton.setAttribute('aria-label', dark ? 'Use light theme' : 'Use dark theme');
    themeButton.title = dark ? 'Switch to light theme' : 'Switch to dark theme';
    themeButton.textContent = dark ? '☀' : '◐';
  }
  updateThemeButton();
  if (themeButton) themeButton.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { window.localStorage.setItem(themeKey, next); } catch (e) { /* Storage can be disabled. */ }
    updateThemeButton();
  });
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      try {
        if (!window.localStorage.getItem(themeKey)) {
          delete root.dataset.theme;
          updateThemeButton();
        }
      } catch (e) { /* The system theme still applies through CSS. */ }
    });
  }

  var menuButton = document.querySelector('.menu-toggle');
  var nav = document.getElementById('primary-nav');
  function closeMenu(returnFocus) {
    if (!menuButton || !nav) return;
    menuButton.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    if (returnFocus) menuButton.focus();
  }
  if (menuButton && nav) {
    menuButton.addEventListener('click', function () {
      var open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      if (!open) {
        var first = nav.querySelector('a');
        if (first) first.focus();
      }
    });
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeMenu(false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
  }

  var sectionLinks = Array.prototype.slice.call(document.querySelectorAll('.nav nav a[href^="#"]'));
  if (sectionLinks.length && 'IntersectionObserver' in window) {
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        sectionLinks.forEach(function (link) {
          if (link.getAttribute('href') === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-22% 0px -68% 0px' });
    sectionLinks.forEach(function (link) {
      var target = document.getElementById(link.getAttribute('href').slice(1));
      if (target) sectionObserver.observe(target);
    });
  }

  document.querySelectorAll('[data-copy-email]').forEach(function (button) {
    button.addEventListener('click', async function () {
      var email = button.getAttribute('data-copy-email');
      var status = document.querySelector('.copy-status');
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(email);
        } else {
          var field = document.createElement('textarea');
          field.value = email;
          field.setAttribute('readonly', '');
          field.style.position = 'fixed';
          field.style.opacity = '0';
          document.body.appendChild(field);
          field.select();
          var copied = document.execCommand('copy');
          field.remove();
          if (!copied) throw new Error('Copy command unavailable');
        }
        if (status) status.textContent = 'Email address copied.';
      } catch (error) {
        if (status) status.textContent = 'Copy was unavailable. Email: ' + email;
      }
    });
  });

  document.querySelectorAll('[data-image-dialog]').forEach(function (trigger) {
    var dialog = document.getElementById(trigger.getAttribute('data-image-dialog'));
    if (!dialog) return;
    var close = dialog.querySelector('[data-dialog-close]');
    var previous = null;
    trigger.addEventListener('click', function () {
      previous = trigger;
      if (typeof dialog.showModal === 'function') dialog.showModal();
      else dialog.setAttribute('open', '');
      if (close) close.focus();
    });
    if (close) close.addEventListener('click', function () {
      if (typeof dialog.close === 'function') dialog.close();
      else dialog.removeAttribute('open');
    });
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) {
        if (typeof dialog.close === 'function') dialog.close();
        else dialog.removeAttribute('open');
      }
    });
    dialog.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab') return;
      var targets = Array.prototype.slice.call(dialog.querySelectorAll('button, a[href], [tabindex]:not([tabindex="-1"])'))
        .filter(function (el) { return !el.disabled && !el.hidden; });
      if (!targets.length) { event.preventDefault(); return; }
      var first = targets[0], last = targets[targets.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    dialog.addEventListener('close', function () { if (previous) previous.focus(); });
    dialog.addEventListener('cancel', function () { if (previous) previous.focus(); });
  });
})();
