// Internal links: every href="/..." in docs/ resolved against the pages that
// exist. Also reports orphans, which are usually a nav entry someone forgot.
//
// No server needed, it reads the files.
//
import { readdirSync, statSync, readFileSync, existsSync } from 'fs';
const SITE = p => !p.startsWith('/internal/');

function walk(d, base=''){let o=[];for(const f of readdirSync(d)){const p=d+'/'+f;if(statSync(p).isDirectory())o=o.concat(walk(p,base+'/'+f));else if(f.endsWith('.html'))o.push(base+'/'+f);}return o;}
const pages = walk('docs').filter(SITE);
const have = new Set(pages.map(p=>p.replace(/\.html$/,'').replace(/\/index$/,'/')));
have.add('/');
const targets = new Map();
for (const p of pages) {
  const html = readFileSync('docs'+p,'utf8');
  for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
    const h = m[1];
    if (/\.(png|jpg|svg|ico|xml|txt|js|css|webmanifest)$/.test(h)) continue;
    if (!targets.has(h)) targets.set(h, new Set());
    targets.get(h).add(p);
  }
}
let broken = 0;
for (const [h, from] of [...targets].sort()) {
  const ok = have.has(h) || have.has(h.replace(/\/$/,'')) || existsSync('docs'+h) || existsSync('docs'+h+'.html');
  if (!ok) { broken++; console.log('BROKEN', h, '<- e.g.', [...from][0], `(${from.size} pages)`); }
}
console.log(`\n${pages.length} pages, ${targets.size} distinct internal link targets, ${broken} broken`);
// inbound link counts, to spot orphans
const inbound = new Map(pages.map(p=>[p.replace(/\.html$/,''),0]));
for (const [h, from] of targets) { const k=h.replace(/\/$/,''); if (inbound.has(k)) inbound.set(k, from.size); }
const orphans=[...inbound].filter(([k,v])=>v===0 && k!=='/index');
console.log('orphan pages (no inbound internal links):', orphans.length ? orphans.map(o=>o[0]).join(', ') : 'none');
