(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
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
    menuButton.setAttribute('aria-label', 'Open navigation');
    var menuText = menuButton.querySelector('.sr-only');
    if (menuText) menuText.textContent = 'Open navigation';
    nav.classList.remove('is-open');
    if (returnFocus) menuButton.focus();
  }
  if (menuButton && nav) {
    var menuLabel = menuButton.querySelector('.sr-only');
    function updateMenuLabel(open) {
      if (menuLabel) menuLabel.textContent = open ? 'Close navigation' : 'Open navigation';
      menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    }
    menuButton.addEventListener('click', function () {
      var open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      updateMenuLabel(!open);
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

  /* Keep keyboard focus inside native dialogs, including WebKit builds that do not cycle it. */
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Tab') return;
    var dialog = Array.prototype.slice.call(document.querySelectorAll('dialog[open]')).pop();
    if (!dialog) return;
    var focusable = Array.prototype.slice.call(dialog.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex="-1"])'
    )).filter(function (element) {
      return !element.closest('[hidden]') && element.getAttribute('aria-hidden') !== 'true' && element.getClientRects().length > 0;
    });
    if (!focusable.length) {
      event.preventDefault();
      dialog.focus();
      return;
    }
    var currentIndex = focusable.indexOf(document.activeElement);
    var nextIndex = currentIndex === -1 ? (event.shiftKey ? focusable.length - 1 : 0) :
      (currentIndex + (event.shiftKey ? -1 : 1) + focusable.length) % focusable.length;
    event.preventDefault();
    focusable[nextIndex].focus();
  });

  /* Role disclosures keep every role and every project available in the page. */
  var rolePanels = Array.prototype.slice.call(document.querySelectorAll('[data-role-panel]'));
  var roleStatus = document.getElementById('role-selection-status');
  var syncingRoles = false;
  function setRoleInUrl(roleId, mode) {
    var params = new URLSearchParams(window.location.search);
    if (roleId) params.set('role', roleId);
    else params.delete('role');
    var next = window.location.pathname + (params.toString() ? '?' + params.toString() : '') + '#role-explorer';
    if (mode === 'replace') window.history.replaceState({}, '', next);
    else window.history.pushState({}, '', next);
  }
  function updateRolePanels(roleId) {
    syncingRoles = true;
    rolePanels.forEach(function (panel) {
      var selected = panel.dataset.rolePanel === roleId;
      panel.open = selected;
      var summary = panel.querySelector('summary');
      if (summary) {
        if (selected) summary.setAttribute('aria-current', 'location');
        else summary.removeAttribute('aria-current');
      }
    });
    window.setTimeout(function () { syncingRoles = false; }, 0);
    if (roleStatus) {
      var selectedPanel = rolePanels.find(function (panel) { return panel.dataset.rolePanel === roleId; });
      roleStatus.textContent = selectedPanel ? selectedPanel.querySelector('summary span').textContent.trim() + ' focus selected. Its skills, evidence and project links are expanded; all other work remains available.' : 'Choose a role to see a focused set of skills and project links.';
    }
  }
  if (rolePanels.length) {
    var initialRole = new URLSearchParams(window.location.search).get('role');
    if (!rolePanels.some(function (panel) { return panel.dataset.rolePanel === initialRole; })) initialRole = '';
    updateRolePanels(initialRole);
    rolePanels.forEach(function (panel) {
      panel.addEventListener('toggle', function () {
        if (syncingRoles) return;
        var roleId = panel.open ? panel.dataset.rolePanel : '';
        if (panel.open) rolePanels.forEach(function (other) { if (other !== panel) other.open = false; });
        setRoleInUrl(roleId, 'push');
        updateRolePanels(roleId);
      });
    });
    window.addEventListener('popstate', function () {
      var roleId = new URLSearchParams(window.location.search).get('role');
      if (!rolePanels.some(function (panel) { return panel.dataset.rolePanel === roleId; })) roleId = '';
      updateRolePanels(roleId);
    });
    document.querySelectorAll('[data-role-reset]').forEach(function (button) {
      button.addEventListener('click', function (event) {
        event.preventDefault();
        setRoleInUrl('', 'push');
        updateRolePanels('');
      });
    });
  }

  /* Problem-led project paths are native disclosures with a shareable query state. */
  var focusPanels = Array.prototype.slice.call(document.querySelectorAll('[data-exploration-panel]'));
  var focusStatus = document.getElementById('focus-selection-status');
  var syncingFocus = false;
  function setFocusInUrl(focusId, mode) {
    var params = new URLSearchParams(window.location.search);
    if (focusId) params.set('focus', focusId);
    else params.delete('focus');
    var next = window.location.pathname + (params.toString() ? '?' + params.toString() : '') + '#focus-explorer';
    if (mode === 'replace') window.history.replaceState({}, '', next);
    else window.history.pushState({}, '', next);
  }
  function updateFocusPanels(focusId) {
    syncingFocus = true;
    focusPanels.forEach(function (panel) {
      var selected = panel.dataset.explorationPanel === focusId;
      panel.open = selected;
      var summary = panel.querySelector('summary');
      if (summary) {
        if (selected) summary.setAttribute('aria-current', 'location');
        else summary.removeAttribute('aria-current');
      }
    });
    window.setTimeout(function () { syncingFocus = false; }, 0);
    if (focusStatus) {
      var selectedPanel = focusPanels.find(function (panel) { return panel.dataset.explorationPanel === focusId; });
      var projectCount = selectedPanel ? selectedPanel.querySelectorAll('.focus-projects a').length : 0;
      focusStatus.textContent = selectedPanel ? selectedPanel.querySelector('summary span').textContent.trim() +
        ' selected. ' + projectCount + (projectCount === 1 ? ' project link' : ' project links') + ' and supporting experience are expanded.' :
        'Choose a question to open a focused project path; all six remain available.';
    }
  }
  if (focusPanels.length) {
    var initialFocus = new URLSearchParams(window.location.search).get('focus');
    if (!focusPanels.some(function (panel) { return panel.dataset.explorationPanel === initialFocus; })) initialFocus = '';
    updateFocusPanels(initialFocus);
    focusPanels.forEach(function (panel) {
      panel.addEventListener('toggle', function () {
        if (syncingFocus) return;
        var focusId = panel.open ? panel.dataset.explorationPanel : '';
        if (panel.open) focusPanels.forEach(function (other) { if (other !== panel) other.open = false; });
        setFocusInUrl(focusId, 'push');
        updateFocusPanels(focusId);
      });
    });
    window.addEventListener('popstate', function () {
      var focusId = new URLSearchParams(window.location.search).get('focus');
      if (!focusPanels.some(function (panel) { return panel.dataset.explorationPanel === focusId; })) focusId = '';
      updateFocusPanels(focusId);
    });
    document.querySelectorAll('[data-focus-reset]').forEach(function (link) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        setFocusInUrl('', 'push');
        updateFocusPanels('');
      });
    });
  }

  /* A restrained pointer glow runs only on fine pointers and respects reduced motion. */
  var hero = document.querySelector('.hero-grid');
  var finePointer = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (hero && finePointer && !reduceMotion) {
    var pendingPointer = null;
    hero.addEventListener('pointermove', function (event) {
      if (pendingPointer) return;
      pendingPointer = window.requestAnimationFrame(function () {
        var bounds = hero.getBoundingClientRect();
        hero.style.setProperty('--glow-x', Math.round(event.clientX - bounds.left) + 'px');
        hero.style.setProperty('--glow-y', Math.round(event.clientY - bounds.top) + 'px');
        pendingPointer = null;
      });
    }, { passive: true });
  }

  /* Keep the case-study contents list aligned with the section in view. */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var tocObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (link) {
          if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-18% 0px -72% 0px' });
    tocLinks.forEach(function (link) {
      var target = document.getElementById(link.hash.slice(1));
      if (target) tocObserver.observe(target);
    });
  }

  var returnLink = document.querySelector('[data-project-return]');
  if (returnLink) {
    try {
      var returnState = JSON.parse(window.sessionStorage.getItem('portfolio:project-return') || 'null');
      if (returnState && returnState.url) {
        returnLink.href = returnState.url;
        if (new URLSearchParams(returnState.url.split('?')[1] || '').toString()) {
          returnLink.textContent = 'Back to filtered results';
          returnLink.setAttribute('aria-label', 'Back to filtered project results');
        }
      }
    } catch (error) { /* Direct visits still have a working Projects link. */ }
  }

  /* Enable tab behavior only after JavaScript loads; every panel stays visible without it. */
  document.querySelectorAll('[data-evidence-tabs]').forEach(function (container) {
    var tabs = Array.prototype.slice.call(container.querySelectorAll('[role="tab"]'));
    var tablist = container.querySelector('[role="tablist"]');
    if (!tabs.length || !tablist) return;
    tablist.hidden = false;
    function activate(index, moveFocus) {
      tabs.forEach(function (tab, tabIndex) {
        var selected = tabIndex === index;
        tab.hidden = false;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        var panel = document.getElementById(tab.getAttribute('aria-controls'));
        if (panel) panel.hidden = !selected;
        if (selected && moveFocus) tab.focus();
      });
    }
    tabs.forEach(function (tab, index) {
      tab.hidden = false;
      tab.addEventListener('click', function () { activate(index, false); });
      tab.addEventListener('keydown', function (event) {
        var next = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + tabs.length - 1) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(next, true);
      });
    });
    var selectedIndex = tabs.findIndex(function (tab) { return tab.getAttribute('aria-selected') === 'true'; });
    activate(selectedIndex < 0 ? 0 : selectedIndex, false);
  });

  document.querySelectorAll('[data-architecture-explorer]').forEach(function (explorer) {
    var tabs = Array.prototype.slice.call(explorer.querySelectorAll('[data-architecture-tab]'));
    var panel = explorer.querySelector('[data-architecture-panel]');
    var fallback = explorer.parentElement.querySelector('.architecture-components');
    if (!fallback || !panel || tabs.length === 0) return;
    var components = Array.prototype.slice.call(fallback.querySelectorAll('[data-architecture-item]'));

    function activate(index, moveFocus) {
      if (!components[index]) return;
      tabs.forEach(function (tab, tabIndex) {
        var selected = tabIndex === index;
        tab.setAttribute('aria-selected', selected ? 'true' : 'false');
        tab.tabIndex = selected ? 0 : -1;
      });
      var component = components[index];
      var tab = tabs[index];
      panel.setAttribute('aria-labelledby', tab.id);
      panel.innerHTML = component.querySelector('div').innerHTML;
      if (moveFocus) tab.focus();
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener('click', function () { activate(index, false); });
      tab.addEventListener('keydown', function (event) {
        var next = index;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + tabs.length - 1) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activate(next, true);
      });
    });
    activate(0, false);
    components.forEach(function (component) {
      component.addEventListener('toggle', function () {
        if (!component.open) return;
        components.forEach(function (other) { if (other !== component) other.open = false; });
      });
    });
  });

  var toc = document.getElementById('case-toc');
  if (toc && window.matchMedia('(max-width: 760px)').matches) toc.open = false;

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
    dialog.addEventListener('close', function () { if (previous) previous.focus(); });
    dialog.addEventListener('cancel', function () { if (previous) previous.focus(); });
  });
})();
