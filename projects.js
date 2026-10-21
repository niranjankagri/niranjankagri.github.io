(function () {
  'use strict';
  var form = document.getElementById('project-filters');
  var grid = document.getElementById('project-grid');
  if (!form || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.project-card'));
  var search = document.getElementById('project-search');
  var skill = document.getElementById('skill-search');
  var role = document.getElementById('role-focus');
  var sort = document.getElementById('project-sort');
  var counter = document.getElementById('result-count');
  var empty = document.getElementById('empty-results');
  var active = document.getElementById('active-filters');
  var clear = document.getElementById('clear-filters');
  var details = document.getElementById('filter-details');
  var roleContext = document.getElementById('role-context');
  var compareTray = document.getElementById('compare-tray');
  var compareCount = document.getElementById('compare-count');
  var compareAnnouncement = document.getElementById('compare-announcement');
  var preview = document.getElementById('project-preview');
  var previewContent = document.getElementById('preview-content');
  var compareDialog = document.getElementById('comparison-dialog');
  var comparisonContent = document.getElementById('comparison-content');
  var selectedIds = [];
  var previousFocus = null;
  var roleNames = {
    'senior-sdet': 'Senior SDET',
    'qa-lead': 'QA Lead',
    'automation-architect': 'Automation Architect'
  };

  function checked(name) {
    return Array.prototype.slice.call(form.querySelectorAll('input[name="' + name + '"]:checked')).map(function (input) { return input.value; });
  }

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    skill.value = params.get('skill') || '';
    ['category', 'tech'].forEach(function (name) {
      var wanted = params.getAll(name);
      form.querySelectorAll('input[name="' + name + '"]').forEach(function (input) {
        input.checked = wanted.indexOf(input.value) !== -1;
      });
    });
    role.value = roleNames[params.get('role')] ? params.get('role') : '';
    sort.value = ['recent', 'alpha'].indexOf(params.get('sort')) !== -1 ? params.get('sort') : 'featured';
    selectedIds = params.getAll('compare').filter(function (id, index, list) {
      return cards.some(function (card) { return card.dataset.projectId === id; }) && list.indexOf(id) === index;
    }).slice(0, 3);
    applyFilters();
  }

  function writeUrl(mode) {
    var params = new URLSearchParams();
    var query = search.value.trim();
    var skillQuery = skill.value.trim();
    if (query) params.set('q', query);
    checked('category').forEach(function (value) { params.append('category', value); });
    checked('tech').forEach(function (value) { params.append('tech', value); });
    if (skillQuery) params.set('skill', skillQuery);
    if (role.value) params.set('role', role.value);
    if (sort.value !== 'featured') params.set('sort', sort.value);
    selectedIds.forEach(function (id) { params.append('compare', id); });
    var next = window.location.pathname + (params.toString() ? '?' + params.toString() : '') + window.location.hash;
    if (next !== window.location.pathname + window.location.search + window.location.hash) {
      if (mode === 'replace') window.history.replaceState({}, '', next);
      else window.history.pushState({}, '', next);
    }
  }

  function searchText(card) {
    return (card.dataset.search || '').toLocaleLowerCase();
  }

  function sortCards() {
    var cats = checked('category').map(function (value) { return value.toLocaleLowerCase(); });
    var techs = checked('tech').map(function (value) { return value.toLocaleLowerCase(); });
    var query = search.value.trim().toLocaleLowerCase();
    var skillQuery = skill.value.trim().toLocaleLowerCase();
    var roleId = role.value;
    var order = cards.slice();
    order.sort(function (a, b) {
      var roleOrder = roleId ? Number((b.dataset.roles || '').split(' ').indexOf(roleId) !== -1) - Number((a.dataset.roles || '').split(' ').indexOf(roleId) !== -1) : 0;
      if (roleOrder) return roleOrder;
      if (sort.value === 'alpha') return a.querySelector('.card-title').textContent.localeCompare(b.querySelector('.card-title').textContent);
      if (sort.value === 'recent') {
        var recentOrder = (b.dataset.date || '').localeCompare(a.dataset.date || '');
        if (recentOrder) return recentOrder;
      }
      var featuredOrder = Number(b.dataset.featured === 'true') - Number(a.dataset.featured === 'true');
      return featuredOrder || cards.indexOf(a) - cards.indexOf(b);
    });
    order.forEach(function (card) { grid.appendChild(card); });

    var count = 0;
    var roleMatches = 0;
    cards.forEach(function (card) {
      var text = searchText(card);
      var cardCategories = (card.dataset.category || '').split('|');
      var cardTech = (card.dataset.tech || '').split(' ');
      var matches = (!query || text.indexOf(query) !== -1) &&
        (!skillQuery || text.indexOf(skillQuery) !== -1) &&
        (!cats.length || cats.some(function (value) { return cardCategories.indexOf(value) !== -1; })) &&
        (!techs.length || techs.some(function (value) { return cardTech.indexOf(value) !== -1; }));
      card.hidden = !matches;
      if (matches) {
        count += 1;
        if (roleId && (card.dataset.roles || '').split(' ').indexOf(roleId) !== -1) roleMatches += 1;
      }
      var isRoleMatch = roleId && (card.dataset.roles || '').split(' ').indexOf(roleId) !== -1;
      card.classList.toggle('role-fit', Boolean(isRoleMatch));
      var kind = card.querySelector('.kind');
      if (kind) {
        var badge = kind.querySelector('.role-fit-label');
        if (isRoleMatch && !badge) {
          badge = document.createElement('span');
          badge.className = 'role-fit-label';
          badge.textContent = 'Suggested for ' + roleNames[roleId];
          kind.appendChild(badge);
        } else if (!isRoleMatch && badge) badge.remove();
      }
      var compareButton = card.querySelector('[data-compare-project]');
      if (compareButton) {
        var isSelected = selectedIds.indexOf(card.dataset.projectId) !== -1;
        compareButton.setAttribute('aria-pressed', String(isSelected));
        compareButton.textContent = isSelected ? 'Selected' : 'Compare';
        compareButton.setAttribute('aria-label', (isSelected ? 'Remove ' : 'Add ') + card.querySelector('.card-title').textContent + (isSelected ? ' from comparison' : ' to comparison'));
      }
    });
    counter.textContent = 'Showing ' + count + ' of ' + cards.length + ' projects' + (roleId ? '; ' + roleMatches + ' matching this role are highlighted' : '');
    empty.hidden = count !== 0;
    renderActive();
    renderRoleContext(roleMatches);
    renderCompareTray();
  }

  function applyFilters() {
    sortCards();
  }

  function renderRoleContext(roleMatches) {
    if (!roleContext) return;
    if (!role.value) {
      roleContext.hidden = true;
      roleContext.replaceChildren();
      return;
    }
    roleContext.hidden = false;
    roleContext.textContent = roleMatches + ' projects are highlighted for ' + roleNames[role.value] + '. Other projects stay in the collection and remain searchable.';
  }

  function addChip(label, onRemove, accessibleName) {
    var item = document.createElement('li');
    var text = document.createElement('span');
    text.textContent = label;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'chip-remove';
    button.textContent = 'Remove';
    button.setAttribute('aria-label', accessibleName);
    button.addEventListener('click', function () {
      onRemove();
      writeUrl('push');
      applyFilters();
    });
    item.append(text, button);
    active.appendChild(item);
  }

  function renderActive() {
    active.replaceChildren();
    if (search.value.trim()) addChip('Search: ' + search.value.trim(), function () { search.value = ''; }, 'Remove search filter');
    checked('category').forEach(function (value) {
      addChip('Category: ' + value, function () {
        form.querySelectorAll('input[name="category"]').forEach(function (input) { if (input.value === value) input.checked = false; });
      }, 'Remove category filter ' + value);
    });
    checked('tech').forEach(function (value) {
      addChip('Language: ' + value, function () {
        form.querySelectorAll('input[name="tech"]').forEach(function (input) { if (input.value === value) input.checked = false; });
      }, 'Remove language filter ' + value);
    });
    if (skill.value.trim()) addChip('Skill: ' + skill.value.trim(), function () { skill.value = ''; }, 'Remove skill filter');
    if (role.value) addChip('Role: ' + roleNames[role.value], function () { role.value = ''; }, 'Remove role focus');
    if (sort.value !== 'featured') addChip('Sort: ' + sort.options[sort.selectedIndex].text, function () { sort.value = 'featured'; }, 'Reset project sorting');
    clear.disabled = active.children.length === 0;
  }

  function renderCompareTray() {
    compareTray.hidden = selectedIds.length === 0;
    var label = selectedIds.length + ' project' + (selectedIds.length === 1 ? '' : 's') + ' selected';
    compareCount.textContent = label;
    compareAnnouncement.textContent = label;
    document.getElementById('open-comparison').disabled = selectedIds.length < 2;
    document.getElementById('open-comparison').setAttribute('aria-label', 'Compare ' + label);
  }

  function createElement(tag, className, text) {
    var element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function appendLink(parent, href, text, className, newWindow) {
    if (!href) return;
    var link = createElement('a', className || 'btn', text);
    link.href = href;
    if (newWindow) {
      link.target = '_blank';
      link.rel = 'noopener';
    }
    parent.appendChild(link);
    return link;
  }

  function openPreview(card, trigger) {
    var caseLink = card.querySelector('.card-title a');
    if (!preview || typeof preview.showModal !== 'function') {
      window.location.href = caseLink.href;
      return;
    }
    previousFocus = trigger;
    previewContent.replaceChildren();
    document.getElementById('preview-title').textContent = caseLink.textContent;
    var figure = document.createElement('figure');
    var image = createElement('img', 'preview-image');
    var hasArchitecturePreview = Boolean(card.dataset.architectureImage);
    image.src = hasArchitecturePreview ? card.dataset.architectureImage : card.dataset.image;
    image.alt = hasArchitecturePreview ? card.dataset.architectureAlt : card.dataset.alt;
    if (hasArchitecturePreview) image.classList.add('architecture-thumbnail');
    image.width = 640;
    image.height = 400;
    image.loading = 'lazy';
    figure.appendChild(image);
    figure.appendChild(createElement('figcaption', '', hasArchitecturePreview ? 'Architecture diagram. Component details and source links are in the full case study.' : 'Static project evidence thumbnail. Its date and evidence type are shown below.'));
    var purpose = createElement('p', 'lead', card.dataset.purpose);
    var result = createElement('p', 'fact', card.dataset.result);
    var resultKind = createElement('p', 'evidence-kind', card.dataset.resultKind);
    var architecture = createElement('section', 'preview-architecture');
    architecture.appendChild(createElement('h3', '', 'Architecture and engineering approach'));
    architecture.appendChild(createElement('p', '', card.dataset.approach));
    appendLink(architecture, caseLink.href + '#architecture', 'Open architecture notes', 'text-action', false);
    var evidence = createElement('section', 'preview-evidence');
    evidence.appendChild(createElement('h3', '', 'Evidence'));
    evidence.appendChild(createElement('p', '', card.dataset.evidenceLabel + ' - checked ' + card.dataset.date + '. ' + card.dataset.resultKind));
    var actions = createElement('div', 'btns preview-actions');
    var fullCaseLink = appendLink(actions, caseLink.href, 'Open full case study', 'btn primary', false);
    fullCaseLink.dataset.caseLink = 'true';
    appendLink(actions, card.dataset.source, 'Source', 'btn', true);
    appendLink(actions, card.dataset.live, 'Live demo', 'btn live-action', true);
    appendLink(actions, card.dataset.evidenceUrl, card.dataset.evidenceLabel, 'btn', true);
    appendLink(actions, card.dataset.reportUrl, 'Report asset', 'btn', true);
    previewContent.append(figure, purpose, result, resultKind, architecture, evidence, actions);
    preview.showModal();
    var close = preview.querySelector('[data-dialog-close]');
    if (close) close.focus();
  }

  function selectedCards() {
    return selectedIds.map(function (id) { return cards.find(function (card) { return card.dataset.projectId === id; }); }).filter(Boolean);
  }

  function renderComparison() {
    comparisonContent.replaceChildren();
    var projects = selectedCards();
    var dimensions = [
      ['Languages', 'languages'],
      ['Test layers', 'layers'],
      ['Browsers or devices', 'targets'],
      ['CI approach', 'workflowName'],
      ['Reporting', 'report'],
      ['Key engineering decisions', 'approach'],
      ['Known limitations and evidence scope', 'comparisonLimits']
    ];
    function valueFor(card, key) {
      if (key === 'workflowName') return card.dataset.workflow ? 'GitHub Actions / ' + card.dataset.workflowName : 'No automated workflow is configured.';
      if (key === 'comparisonLimits') return card.dataset.comparisonLimits;
      return card.dataset[key];
    }
    function addDimensionLinks(parent, card, key) {
      if (key === 'report') appendLink(parent, card.dataset.reportUrl, 'Open report asset', 'inline-link', true);
      if (key === 'workflowName' && card.dataset.workflow) appendLink(parent, card.dataset.workflow, 'Open workflow history', 'inline-link', true);
      if (key === 'comparisonLimits') appendLink(parent, card.dataset.case, 'Read case-study limitations', 'inline-link', false);
    }
    var tableWrap = createElement('div', 'table-wrap comparison-table-wrap');
    var table = document.createElement('table');
    table.className = 'comparison-table';
    var head = document.createElement('thead');
    var headRow = document.createElement('tr');
    var dimensionHeading = createElement('th', '', 'Dimension');
    dimensionHeading.scope = 'col';
    headRow.appendChild(dimensionHeading);
    projects.forEach(function (card) {
      var th = createElement('th', '', card.querySelector('.card-title').textContent);
      th.scope = 'col';
      headRow.appendChild(th);
    });
    head.appendChild(headRow);
    var body = document.createElement('tbody');
    dimensions.forEach(function (dimension) {
      var row = document.createElement('tr');
      var th = createElement('th', '', dimension[0]);
      th.scope = 'row';
      row.appendChild(th);
      projects.forEach(function (card) {
        var cell = document.createElement('td');
        var key = dimension[1];
        var value = valueFor(card, key);
        cell.textContent = value || 'See case study for details.';
        addDimensionLinks(cell, card, key);
        row.appendChild(cell);
      });
      body.appendChild(row);
    });
    table.append(head, body);
    tableWrap.appendChild(table);
    comparisonContent.appendChild(tableWrap);
    var mobile = createElement('div', 'comparison-mobile');
    projects.forEach(function (card) {
      var article = document.createElement('article');
      article.appendChild(createElement('h3', '', card.querySelector('.card-title').textContent));
      var list = document.createElement('dl');
      dimensions.forEach(function (dimension) {
        var key = dimension[1];
        var dt = createElement('dt', '', dimension[0]);
        var dd = createElement('dd', '', valueFor(card, key) || 'See case study for details.');
        addDimensionLinks(dd, card, key);
        list.append(dt, dd);
      });
      article.appendChild(list);
      mobile.appendChild(article);
    });
    comparisonContent.appendChild(mobile);
    var note = createElement('p', 'comparison-note', 'Comparison fields describe checked-in project records. A workflow link identifies the configured workflow; it does not imply that a run is live.');
    comparisonContent.appendChild(note);
  }

  function rememberReturn() {
    try {
      sessionStorage.setItem('portfolio:project-return', JSON.stringify({
        url: window.location.pathname + window.location.search + window.location.hash,
        scrollY: window.scrollY
      }));
    } catch (error) { /* Private browsing can disable storage; browser Back still works. */ }
  }

  form.querySelectorAll('input[type="checkbox"]').forEach(function (input) {
    input.addEventListener('change', function () { writeUrl('push'); applyFilters(); });
  });
  search.addEventListener('input', function () { writeUrl('replace'); applyFilters(); });
  skill.addEventListener('input', function () { writeUrl('replace'); applyFilters(); });
  role.addEventListener('change', function () { writeUrl('push'); applyFilters(); });
  sort.addEventListener('change', function () { writeUrl('push'); applyFilters(); });
  clear.addEventListener('click', function () {
    search.value = '';
    skill.value = '';
    role.value = '';
    sort.value = 'featured';
    form.querySelectorAll('input[type="checkbox"]').forEach(function (input) { input.checked = false; });
    selectedIds = [];
    writeUrl('push');
    applyFilters();
    search.focus();
  });
  window.addEventListener('popstate', readUrl);
  grid.addEventListener('click', function (event) {
    var previewButton = event.target.closest('[data-preview-project]');
    if (previewButton) {
      event.preventDefault();
      openPreview(previewButton.closest('.project-card'), previewButton);
      return;
    }
    var compareButton = event.target.closest('[data-compare-project]');
    if (compareButton) {
      var card = compareButton.closest('.project-card');
      var id = card.dataset.projectId;
      var currentIndex = selectedIds.indexOf(id);
      if (currentIndex !== -1) selectedIds.splice(currentIndex, 1);
      else if (selectedIds.length >= 3) {
        compareAnnouncement.textContent = 'You can compare up to three projects. Remove one selection first.';
        return;
      } else selectedIds.push(id);
      writeUrl('push');
      applyFilters();
      return;
    }
    var skillLink = event.target.closest('.tag-link');
    if (skillLink) {
      event.preventDefault();
      skill.value = skillLink.textContent.trim();
      writeUrl('push');
      applyFilters();
      document.getElementById('results-title').focus();
    }
    var caseLink = event.target.closest('.card-title a, .actions .go, .card-image');
    if (caseLink) rememberReturn();
  });
  document.addEventListener('click', function (event) {
    if (event.target.closest('[data-case-link]')) rememberReturn();
  });

  function closeDialog(dialog) {
    if (dialog && dialog.open) dialog.close();
  }
  document.querySelectorAll('dialog [data-dialog-close]').forEach(function (button) {
    button.addEventListener('click', function () { closeDialog(button.closest('dialog')); });
  });
  [preview, compareDialog].forEach(function (dialog) {
    if (!dialog) return;
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) closeDialog(dialog);
    });
    dialog.addEventListener('close', function () {
      if (previousFocus && document.contains(previousFocus)) previousFocus.focus();
      previousFocus = null;
    });
    dialog.addEventListener('cancel', function () {
      if (previousFocus && document.contains(previousFocus)) previousFocus.focus();
    });
  });
  document.getElementById('open-comparison').addEventListener('click', function () {
    if (selectedIds.length < 2 || typeof compareDialog.showModal !== 'function') return;
    previousFocus = document.getElementById('open-comparison');
    renderComparison();
    compareDialog.showModal();
    var close = compareDialog.querySelector('[data-dialog-close]');
    if (close) close.focus();
  });
  document.getElementById('clear-comparison').addEventListener('click', function () {
    selectedIds = [];
    writeUrl('push');
    applyFilters();
  });

  window.addEventListener('pageshow', function (event) {
    try {
      var saved = JSON.parse(sessionStorage.getItem('portfolio:project-return') || 'null');
      if (saved && saved.url === window.location.pathname + window.location.search + window.location.hash) {
        requestAnimationFrame(function () { window.scrollTo(0, saved.scrollY); });
        sessionStorage.removeItem('portfolio:project-return');
      }
    } catch (error) { /* Browser Back retains the native scroll-restoration behavior. */ }
  });

  readUrl();
  if (window.matchMedia('(max-width: 760px)').matches && !window.location.search) details.open = false;
})();
