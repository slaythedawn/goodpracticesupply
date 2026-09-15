// Header search. Plain DOM, deliberately outside the page components: every
// page on this site is a hydrated component, and an overlay that lives in the
// React tree would have to be added to all eighty-one of them. This attaches
// itself to whatever search control it finds and owns its own markup.
//
// The index is docs/search-index.json, written by gen/searchindex.py. It is
// fetched once, on first open, so it costs nothing on a page nobody searches.
(function () {
  'use strict';
  var FOREST = '#143026', INK = '#0E0E0E', GRAPHITE = '#59595A';
  var HAIRLINE = '#E3E3E1', CANVAS = '#FAFAFA', PLATE = '#EDEDEB', MINT = '#8FBFA6';
  var MONO = "font-family:'IBM Plex Mono',monospace;font-weight:500";
  var SANS = "font-family:'Archivo',sans-serif";
  var POPULAR = ['/shop/syringes-needles/u-100-insulin-syringes',
                 '/shop/diluents-swabs/alcohol-swabs',
                 '/shop/gloves-ppe/nitrile-examination-gloves',
                 '/gauge-finder',
                 '/shop/syringes-needles/pen-needles'];

  var rows = null, loading = false, el = null, input = null, list = null;
  var results = [], cursor = 0, lastFocus = null;

  function norm(s) { return (s || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' '); }

  function score(row, q) {
    var t = norm(row.t), k = row.k || '';
    if (t === q) return 100;
    if (t.indexOf(q) === 0) return 90;
    // A word in the name starting with the query: "gauze" finds "Sterile gauze swabs".
    if ((' ' + t).indexOf(' ' + q) > -1) return 80;
    if (t.indexOf(q) > -1) return 60;
    if ((' ' + k).indexOf(' ' + q) > -1) return 50;
    if (k.indexOf(q) > -1) return 30;
    return 0;
  }

  function search(raw) {
    var q = norm(raw).trim();
    if (!q || !rows) return [];
    var terms = q.split(/\s+/);
    var out = [];
    for (var i = 0; i < rows.length; i++) {
      var best = 0, all = true;
      for (var j = 0; j < terms.length; j++) {
        var s = score(rows[i], terms[j]);
        if (!s) { all = false; break; }
        if (s > best) best = s;
      }
      // Every word has to land somewhere, so "insulin syringe" does not match
      // everything that merely mentions insulin.
      if (all) out.push({ row: rows[i], s: best + (rows[i].g === 'Category' ? 5 : 0) });
    }
    out.sort(function (a, b) { return b.s - a.s || a.row.t.length - b.row.t.length; });
    return out.slice(0, 8).map(function (o) { return o.row; });
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function render() {
    if (!list) return;
    var q = input.value.trim();
    if (!rows && loading) { list.innerHTML = row_msg('Loading…'); return; }
    if (!q) {
      results = rows ? POPULAR.map(find).filter(Boolean) : [];
      list.innerHTML = results.length
        ? '<div style="' + MONO + ';font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:' + GRAPHITE + ';padding:14px 20px 8px">Popular</div>' + results.map(item).join('')
        : '';
      cursor = 0; paint(); return;
    }
    results = search(q);
    if (!results.length) {
      list.innerHTML = row_msg('Nothing matches “' + esc(q) + '”.')
        + item({ t: 'Gauge Finder', s: 'Not sure what you need? Answer three questions.', u: '/gauge-finder', g: 'Tools' })
        + item({ t: 'Contact us', s: 'Ask a person. We answer seven days.', u: '/contact', g: 'Company' });
      results = [{ u: '/gauge-finder' }, { u: '/contact' }];
      // The message is not selectable, so the first real row is index 0.
      cursor = 0; paint(); return;
    }
    list.innerHTML = results.map(item).join('');
    cursor = 0; paint();
  }

  function row_msg(t) {
    return '<div style="padding:20px 20px 10px;font-size:15px;color:' + GRAPHITE + '">' + t + '</div>';
  }

  function find(u) {
    for (var i = 0; i < rows.length; i++) if (rows[i].u === u) return rows[i];
    return null;
  }

  function item(r) {
    return '<a href="' + esc(r.u) + '" data-gp-sr style="display:flex;align-items:baseline;gap:14px;'
      + 'padding:13px 20px;text-decoration:none;color:' + INK + '">'
      + '<span style="' + SANS + ';font-size:16px;font-weight:600;flex:none">' + esc(r.t) + '</span>'
      + '<span style="font-size:14px;color:' + GRAPHITE + ';overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + esc(r.s || '') + '</span>'
      + '<span style="' + MONO + ';font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:' + GRAPHITE + ';margin-left:auto;flex:none">' + esc(r.g || '') + '</span>'
      + '</a>';
  }

  function paint() {
    var nodes = list.querySelectorAll('[data-gp-sr]');
    for (var i = 0; i < nodes.length; i++) {
      var on = i === cursor;
      nodes[i].style.background = on ? PLATE : 'transparent';
      nodes[i].setAttribute('aria-selected', on ? 'true' : 'false');
      if (on && nodes[i].scrollIntoView) nodes[i].scrollIntoView({ block: 'nearest' });
    }
  }

  function load() {
    if (rows || loading) return;
    loading = true;
    fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (d) {
      rows = d; loading = false; render();
    }).catch(function () {
      loading = false;
      if (list) list.innerHTML = row_msg('Search is unavailable just now. Try the shop.');
    });
  }

  function build() {
    el = document.createElement('div');
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-label', 'Search');
    el.style.cssText = 'position:fixed;inset:0;z-index:9000;display:none;'
      + 'background:rgba(11,26,21,.52);backdrop-filter:blur(3px);padding:clamp(16px,8vh,110px) 16px 16px';
    el.innerHTML =
      '<div data-gp-sbox style="max-width:660px;margin:0 auto;background:' + CANVAS + ';border-radius:24px;'
      + 'border:1px solid ' + HAIRLINE + ';box-shadow:0 30px 80px rgba(11,26,21,.3);overflow:hidden">'
      + '<div style="display:flex;align-items:center;gap:12px;padding:16px 20px;border-bottom:1px solid ' + HAIRLINE + '">'
      + '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true" style="flex:none;color:' + FOREST + '">'
      + '<circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.6"></circle>'
      + '<path d="m12.5 12.5 3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"></path></svg>'
      + '<input data-gp-sinput type="search" autocomplete="off" spellcheck="false" placeholder="Search products and guides" '
      + 'aria-label="Search products and guides" style="' + SANS + ';flex:1;min-width:0;border:0;outline:0;background:transparent;'
      + 'font-size:17px;color:' + INK + ';padding:4px 0">'
      + '<button type="button" data-gp-sclose aria-label="Close search" style="' + MONO + ';flex:none;cursor:pointer;'
      + 'background:transparent;border:1px solid ' + HAIRLINE + ';border-radius:8px;color:' + GRAPHITE + ';font-size:11px;padding:5px 8px">Esc</button>'
      + '</div>'
      + '<div data-gp-slist role="listbox" aria-label="Search results" style="max-height:min(56vh,440px);overflow:auto;padding:6px 0"></div>'
      + '<div style="' + MONO + ';font-size:11px;color:' + GRAPHITE + ';padding:11px 20px;border-top:1px solid ' + HAIRLINE + ';background:' + PLATE + '">'
      + 'Consumables only. We do not supply peptides, hormones or any prescription medicine.</div>'
      + '</div>';
    document.body.appendChild(el);
    input = el.querySelector('[data-gp-sinput]');
    list = el.querySelector('[data-gp-slist]');

    el.addEventListener('mousedown', function (e) { if (e.target === el) close(); });
    el.querySelector('[data-gp-sclose]').addEventListener('click', close);
    input.addEventListener('input', render);
    list.addEventListener('mousemove', function (e) {
      var a = e.target.closest ? e.target.closest('[data-gp-sr]') : null;
      if (!a) return;
      var nodes = [].slice.call(list.querySelectorAll('[data-gp-sr]'));
      var i = nodes.indexOf(a);
      if (i > -1 && i !== cursor) { cursor = i; paint(); }
    });
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      var n = list.querySelectorAll('[data-gp-sr]').length;
      if (e.key === 'ArrowDown' && n) { e.preventDefault(); cursor = (cursor + 1) % n; paint(); }
      else if (e.key === 'ArrowUp' && n) { e.preventDefault(); cursor = (cursor - 1 + n) % n; paint(); }
      else if (e.key === 'Enter' && n) {
        e.preventDefault();
        var a = list.querySelectorAll('[data-gp-sr]')[cursor];
        if (a) window.location.href = a.getAttribute('href');
      }
    });
  }

  function open() {
    if (!el) build();
    lastFocus = document.activeElement;
    el.style.display = 'block';
    document.documentElement.style.overflow = 'hidden';
    load();
    render();
    input.value = '';
    input.focus();
  }

  function close() {
    if (!el) return;
    el.style.display = 'none';
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function isOpen() { return el && el.style.display === 'block'; }

  // The control is rendered by the page component, so it may not exist yet and
  // may be replaced on a re-render. Delegate from the document instead of
  // binding to the node.
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-gp-search], [aria-label="Search"]') : null;
    if (!t) return;
    e.preventDefault();
    open();
  });

  document.addEventListener('keydown', function (e) {
    if (isOpen()) return;
    var tag = (document.activeElement && document.activeElement.tagName) || '';
    var typing = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT'
      || (document.activeElement && document.activeElement.isContentEditable);
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); return; }
    if (e.key === '/' && !typing && !e.metaKey && !e.ctrlKey && !e.altKey) { e.preventDefault(); open(); }
  });
})();
