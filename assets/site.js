// Shared behaviour for the service pages and the English page: theme, mobile menu, footer year, click tracking.
(function(){
  var root = document.documentElement;
  try { var t = localStorage.getItem('theme'); if (t) root.dataset.theme = t; } catch (e) {}
  var themeBtn = document.getElementById('theme');
  if (themeBtn) themeBtn.addEventListener('click', function(){
    var dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
  });
  var menu = document.getElementById('menu'), links = document.getElementById('links');
  if (menu && links) menu.addEventListener('click', function(){ var o = links.classList.toggle('open'); menu.setAttribute('aria-expanded', o); });
  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

  // Visitor stats: counts page views and key clicks once GoatCounter is switched on in agentiq-config.js.
  // Until then this does nothing and sends nothing.
  window.agentiqTrack = function(name){
    try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: 'click/' + name, title: name, event: true }); } catch (e) {}
  };
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href*="wa.me"], a[href^="tel:"], [data-track]');
    if (!a) return;
    var name = a.dataset.track || (a.href.indexOf('wa.me') > -1 ? 'whatsapp' : 'call');
    window.agentiqTrack(name + ':' + location.pathname);
  });
})();
