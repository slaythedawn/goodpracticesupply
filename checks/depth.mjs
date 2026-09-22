// Click depth from the home page, measured in the rendered DOM.
//
// Two reasons it cannot be done by reading the HTML. Most hrefs on this site are
// written by the page component at hydration, so the source contains a fraction
// of the real links: the Learn index looks like it links to one guide and
// actually links to nine. And the local static server redirects /learn to a
// directory listing of docs/learn/, so a path that works on Vercel with
// cleanUrls does not work here. Both of those produced confident wrong answers
// before this file existed.
//
// A page far from the home page, or with no path to it at all, is discovered
// late and carries little internal authority. On a domain with no external
// links that is most of the authority there is.
//
// Needs a static server on 8777:  cd docs && python3 -m http.server 8777
//
import { chromium as loadChromium } from './browser.mjs';
const chromium = await loadChromium();
import { readdirSync, statSync } from 'fs';

const MAX_DEPTH = 3;

function walk(d, base = '') {
  let o = [];
  for (const f of readdirSync(d)) {
    const p = d + '/' + f;
    if (statSync(p).isDirectory()) o = o.concat(walk(p, base + '/' + f));
    else if (f.endsWith('.html')) o.push(base + '/' + f);
  }
  return o;
}

const all = walk('docs').filter(p => !p.startsWith('/internal/'));
// cleanUrls means /shop/x is served from /shop/x.html. Links are written
// without the extension, so both spellings have to map to the same node.
const canon = p => p.replace(/\.html$/, '').replace(/\/index$/, '') || '/';
const known = new Map(all.map(p => [canon(p), p]));

const b = await chromium.launch();
const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
const links = new Map();

for (const p of all) {
  await pg.goto('http://127.0.0.1:8777' + p, { waitUntil: 'networkidle', timeout: 25000 })
          .catch(() => {});
  const hrefs = await pg.evaluate(() =>
    [...document.querySelectorAll('a[href^="/"]')].map(a => a.getAttribute('href')));
  const out = new Set();
  for (const h of hrefs) {
    const c = canon(h.split('#')[0].split('?')[0].replace(/\/$/, '') || '/');
    if (known.has(c) && known.get(c) !== p) out.add(known.get(c));
  }
  links.set(p, out);
}
await b.close();

const home = '/index.html';
const dist = new Map([[home, 0]]);
const queue = [home];
while (queue.length) {
  const cur = queue.shift();
  for (const next of links.get(cur) || []) {
    if (!dist.has(next)) { dist.set(next, dist.get(cur) + 1); queue.push(next); }
  }
}

const hist = new Map();
for (const d of dist.values()) hist.set(d, (hist.get(d) || 0) + 1);
console.log(`${all.length} pages, reachable from the home page in:`);
for (const d of [...hist.keys()].sort((a, c) => a - c))
  console.log(`  ${d} click${d === 1 ? '' : 's'}: ${hist.get(d)}`);

const unreachable = all.filter(p => !dist.has(p));
const deep = all.filter(p => dist.has(p) && dist.get(p) > MAX_DEPTH);
for (const p of unreachable) console.log('FAIL no path from the home page: ' + p);
for (const p of deep) console.log(`FAIL ${dist.get(p)} clicks from home: ${p}`);

const bad = unreachable.length + deep.length;
console.log(bad ? `\n${bad} page${bad === 1 ? '' : 's'} beyond ${MAX_DEPTH} clicks or unreachable`
                : `\nevery page is within ${MAX_DEPTH} clicks of the home page`);
process.exit(bad ? 1 : 0);
