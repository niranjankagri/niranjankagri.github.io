(function () {
  'use strict';
  var form = document.getElementById('project-filters');
  var grid = document.getElementById('project-grid');
  if (!form || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.project-card'));
  var search = document.getElementById('project-search');
  var counter = document.getElementById('result-count');
  var empty = document.getElementById('empty-results');
  var active = document.getElementById('active-filters');
  var clear = document.getElementById('clear-filters');
  var searchHistoryEntry = false;

  function selected(name) {
    return Array.prototype.slice.call(form.querySelectorAll('input[name="' + name + '"]:checked')).map(function (el) { return el.value; });
  }

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    ['category', 'tech'].forEach(function (name) {
      var wanted = params.getAll(name);
      form.querySelectorAll('input[name="' + name + '"]').forEach(function (input) {
        input.checked = wanted.indexOf(input.value) !== -1;
      });
    });
    searchHistoryEntry = false;
    applyFilters();
  }

  function writeUrl(mode) {
    var params = new URLSearchParams();
    var q = search.value.trim();
    if (q) params.set('q', q);
    selected('category').forEach(function (v) { params.append('category', v); });
    selected('tech').forEach(function (v) { params.append('tech', v); });
    var next = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    if (mode === 'replace' || searchHistoryEntry) window.history.replaceState({}, '', next);
    else window.history.pushState({}, '', next);
    if (mode === 'search') searchHistoryEntry = true;
    else searchHistoryEntry = false;
  }

  function applyFilters() {
    var q = search.value.trim().toLocaleLowerCase();
    var cats = selected('category').map(function (x) { return x.toLocaleLowerCase(); });
    var techs = selected('tech').map(function (x) { return x.toLocaleLowerCase(); });
    var count = 0;
    cards.forEach(function (card) {
      var text = card.dataset.search || '';
      var cardCats = (card.dataset.category || '').split('|');
      var cardTechs = (card.dataset.tech || '').split(' ');
      var match = (!q || text.indexOf(q) !== -1) &&
        (!cats.length || cats.some(function (value) { return cardCats.indexOf(value.toLocaleLowerCase()) !== -1; })) &&
        (!techs.length || techs.some(function (value) { return cardTechs.indexOf(value.toLocaleLowerCase()) !== -1; }));
      card.hidden = !match;
      if (match) count += 1;
    });
    counter.textContent = 'Showing ' + count + ' of ' + cards.length + ' projects';
    empty.hidden = count !== 0;
    renderActive(q, cats, techs);
  }

  function renderActive(q, cats, techs) {
    active.replaceChildren();
    var values = [];
    if (q) values.push('Search: ' + search.value.trim());
    selected('category').forEach(function (value) { values.push('Category: ' + value); });
    selected('tech').forEach(function (value) { values.push('Language: ' + value); });
    values.forEach(function (value) {
      var item = document.createElement('li');
      item.textContent = value;
      active.appendChild(item);
    });
    clear.disabled = values.length === 0;
    clear.setAttribute('aria-disabled', values.length === 0 ? 'true' : 'false');
  }

  form.querySelectorAll('input[type="checkbox"]').forEach(function (input) {
    input.addEventListener('change', function () {
      writeUrl('push');
      applyFilters();
    });
  });
  search.addEventListener('input', function () {
    writeUrl('search');
    applyFilters();
  });
  clear.addEventListener('click', function () {
    search.value = '';
    form.querySelectorAll('input[type="checkbox"]').forEach(function (input) { input.checked = false; });
    writeUrl('push');
    applyFilters();
    search.focus();
  });
  window.addEventListener('popstate', readUrl);
  readUrl();

  document.querySelectorAll('.badge-link .ci').forEach(function (image) {
    image.addEventListener('error', function () {
      image.hidden = true;
      var fallback = image.nextElementSibling;
      if (fallback) fallback.hidden = false;
    }, { once: true });
  });
})();
