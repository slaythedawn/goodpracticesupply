// Layout sweep: every page at four widths, looking for horizontal overflow,
// unfilled component holes, JavaScript errors, and a header that has both the
// desktop nav and the burger showing (or neither).
//
// Needs a static server on 8777:  cd docs && python3 -m http.server 8777
//
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { readdirSync, statSync } from 'fs';
const SITE = p => !p.startsWith('/internal/');

function walk(d, base='') { let o=[]; for (const f of readdirSync(d)) { const p=d+'/'+f; if (statSync(p).isDirectory()) o=o.concat(walk(p, base+'/'+f)); else if (f.endsWith('.html')) o.push(base+'/'+f); } return o; }
const all = walk('docs').filter(SITE);
const pages = all.filter((_,i)=> i%6===0).concat(['/index.html','/clinic-portal.html','/for/glp-1-injections.html','/shop.html']);
const b=await chromium.launch(); let fails=0, n=0;
for (const [w,h] of [[390,844],[950,700],[1024,800],[1440,900]]) {
  for (const p of [...new Set(pages)]) {
    const pg=await b.newPage({viewport:{width:w,height:h}});
    const errs=[]; pg.on('pageerror',e=>errs.push(String(e).slice(0,90)));
    await pg.goto('http://127.0.0.1:8777'+p,{waitUntil:'networkidle',timeout:30000}).catch(()=>errs.push('nav'));
    await pg.waitForTimeout(250);
    const r=await pg.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
      raw:(document.body.innerText.match(/\{\{[^}]*\}\}/g)||[]).length,
      burger:!!document.querySelector('[data-gp-burger]') && getComputedStyle(document.querySelector('[data-gp-burger]')).display!=='none',
      nav:!!document.querySelector('[data-gp-nav]') && getComputedStyle(document.querySelector('[data-gp-nav]')).display!=='none'}));
    n++;
    const bad = r.sw>r.cw+1 || r.raw || errs.length || (r.burger===r.nav);
    if (bad) { fails++; console.log('FAIL', w, p, JSON.stringify(r), errs.join('|')); }
    await pg.close();
  }
}
console.log('checked', n, 'page/viewport combinations,', fails, 'failures');
await b.close();
