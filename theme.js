// Light/dark toggle: the saved choice wins over the system setting (set early in <head>)
(function () {
  var root = document.documentElement, key = 'na-theme', button = document.getElementById('theme');
  if (!button) return;
  button.addEventListener('click', function () {
    var dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem(key, root.dataset.theme); } catch (e) {}
  });
})();
