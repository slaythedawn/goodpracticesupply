// SEO check across every page written to rank: the shop, the ten guides under
// /learn and the six protocol pages under /for. Title and description length,
// canonical, Open Graph, exactly one h1, parseable structured data, word count,
// and that every title and description is unique.
//
// It covered only /shop until four guide descriptions were found long enough to
// be truncated in a result. The guides are the pages actually open to indexing,
// so leaving them out was checking the part that does not currently matter.
//
// Needs a static server on 8777:  cd docs && python3 -m http.server 8777
//
import { chromium as loadChromium } from './browser.mjs';
const chromium = await loadChromium();
import { readdirSync, statSync } from 'fs';
const SITE = p => !p.startsWith('/internal/');

function walk(d, base=''){let o=[];for(const f of readdirSync(d)){const p=d+'/'+f;if(statSync(p).isDirectory())o=o.concat(walk(p,base+'/'+f));else if(f.endsWith('.html'))o.push(base+'/'+f);}return o;}
const SECTION = p => p.startsWith('/shop') ? 'shop'
                   : p.startsWith('/learn/') ? 'learn'
                   : p.startsWith('/for/') ? 'for' : null;
const all = walk('docs').filter(SITE).filter(p => SECTION(p));
const b = await chromium.launch();
const pg = await b.newPage({viewport:{width:1280,height:900}});
let bad=0, titles=new Set(), descs=new Set(); const counts={shop:0,learn:0,for:0};
for (const p of all) {
  const errs=[]; const h=e=>errs.push(String(e).slice(0,80)); pg.on('pageerror',h);
  await pg.goto('http://127.0.0.1:8777'+p,{waitUntil:'domcontentloaded',timeout:20000}).catch(()=>errs.push('nav'));
  const r = await pg.evaluate(()=>{
    const g=s=>document.querySelector(s);
    const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{return JSON.parse(s.textContent)['@type']}catch(e){return 'PARSE_ERROR'}});
    return {
      title:(document.title||'').trim(),
      desc:(g('meta[name="description"]')||{}).content||'',
      canon:(g('link[rel="canonical"]')||{}).href||'',
      og:!!g('meta[property="og:title"]'),
      robots:((g('meta[name="robots"]')||{}).content)||'',
      h1:document.querySelectorAll('h1').length,
      h2:document.querySelectorAll('h2').length,
      ld,
      words:(document.body.innerText.match(/\S+/g)||[]).length,
      holes:(document.body.innerText.match(/\{\{[^}]*\}\}/g)||[]).length,
      links:new Set([...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href'))).size,
    };});
  pg.off('pageerror',h);
  const probs=[];
  if(!r.title||r.title.length>75) probs.push('title '+r.title.length);
  if(!r.desc||r.desc.length<70||r.desc.length>170) probs.push('desc '+r.desc.length);
  if(!r.canon) probs.push('no canonical');
  if(!r.og) probs.push('no og');
  if(r.h1!==1) probs.push('h1='+r.h1);
  if(r.ld.includes('PARSE_ERROR')) probs.push('bad json-ld');
  // Shop pages always carry three blocks. /learn/needle-gauge-chart carries
  // Article and BreadcrumbList and no FAQPage, because it has no FAQ, so a
  // flat floor of three would be demanding markup for questions nobody asked.
  const floor = SECTION(p)==='shop' ? 3 : 2;
  if(r.ld.length<floor) probs.push('ld='+r.ld.length);
  if(r.words<400) probs.push('thin '+r.words);
  if(r.holes) probs.push('holes '+r.holes);
  if(errs.length) probs.push('js '+errs[0]);
  counts[SECTION(p)]++;
  titles.add(r.title); descs.add(r.desc);
  if(probs.length){bad++;console.log('FAIL',p,probs.join(' | '));}
}
console.log(`\nchecked ${all.length} pages (${counts.shop} shop, ${counts.learn} learn, ${counts.for} for), ${bad} with problems`);
console.log(`unique titles ${titles.size}/${all.length}, unique descriptions ${descs.size}/${all.length}`);
await b.close();
